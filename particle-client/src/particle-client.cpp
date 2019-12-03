/*
 * Project particle-client
 * Description: Send sensor data to a webserver with TCP
 * Author: Nathan Robinson
 * Date:
 */

// Header Files:
#include "Particle.h"
#include "PietteTech_DHT.h"
#include <deque>

// Hardware:
// DHT11 (Grove) for Temperature and Humidity
// Photoresistor for Brightness

// Constants
#define SECONDS_MS 1000
#define QUEUE_MAX_CAPACITY 200
#define WIFI_TIMEOUT_SECONDS 30
#define PUBLISH_RETRIES 3
#define ERR_OK 0

// Feature Flags
#define LOGGING

// Pin Definitions
#define DHTPIN D4
#define LDRPIN A0

#define DHTTYPE DHT11 // DHT 11

// System configuration macros
SYSTEM_MODE(SEMI_AUTOMATIC);
SYSTEM_THREAD(ENABLED);

// Particle Hardware Identifier (first 8 chars)
char deviceID[9];

// Sensor Data Point Structure
struct ReadingPayload
{
  time_t time;         // Unix time
  float temperature;   // Farenheit (degrees)
  float humidity;      // Relative Humidity %
  uint32_t brightness; // Relative brightness 0-4095
};

// Data point for storing sensor readings
ReadingPayload currentReading;

// Global Objects
TCPClient client;
PietteTech_DHT dht(DHTPIN, DHTTYPE);
std::deque<ReadingPayload> messageQueue;
char jsonBuffer[400];

// Operational Parameters
const uint32_t readingPeriod = 5;  // Read every 5 seconds
const uint32_t publishPeriod = 30; // Publish every 30 seconds

// Socket settings
const char *serverAddress = "10.42.0.1";
uint16_t serverPort = 1234;

// State Flags
bool wifiConnected = false;
bool socketConnected = false;

// Start or restart the socket if neccesary
inline void maintainSocket()
{
  if (!client.connected())
  {
    client.connect(serverAddress, serverPort);
  }
}

inline void connectWifi()
{
  // Return if wifi is already established
  if (WiFi.ready())
  {
    return;
  }

  // Connect to WiFi
  WiFi.connect();

  // Wait for wifi to be ready
  wifiConnected = waitFor(WiFi.ready, WIFI_TIMEOUT_SECONDS * SECONDS_MS);

#ifdef LOGGING
  Serial.println(wifiConnected ? "Established Wi-Fi connection." : "Failed to connect to Wi-Fi!");
#endif
}

// Function prototypes
void readSensors();
void publishData();

// Software timers
Timer readTimer(readingPeriod *SECONDS_MS, readSensors);
Timer publishTimer(publishPeriod *SECONDS_MS, publishData);

// Set the device id string
inline void setDeviceID()
{
  // Get string of device id
  const char *id = System.deviceID();
  snprintf(deviceID, sizeof(deviceID), "%s", id);
}

// Initialize sensors and objects
void setup()
{
  // Save the identifier
  setDeviceID();

  // Start serial connection to PC
  Serial.begin(115200);

  // Initialize sensors
  pinMode(LDRPIN, INPUT);
  dht.begin();

  // Connect to WiFi
  connectWifi();

  // Connect to the server
  maintainSocket();

  // Synchronize time with Particle cloud
  Particle.connect();
  if (waitFor(Particle.connected, WIFI_TIMEOUT_SECONDS * SECONDS_MS))
  {
    Particle.syncTime();
  }
#ifdef LOGGING
  else
  {
    Serial.println("Could not synchronize with the Particle cloud!");
  }
#endif

  // Start timers
  readTimer.start();
  publishTimer.start();
}

// Read sensor data and send it to the server
void loop()
{
}

// TESTING
void dhtLoop()
{
  Serial.println();
  Serial.print(": Retrieving information from sensor: ");
  Serial.print("Read sensor: ");

  int result = dht.acquireAndWait(1000); // wait up to 1 sec (default indefinitely)

  switch (result)
  {
  case DHTLIB_OK:
    Serial.println("OK");
    break;
  case DHTLIB_ERROR_CHECKSUM:
    Serial.println("Error\n\r\tChecksum error");
    break;
  case DHTLIB_ERROR_ISR_TIMEOUT:
    Serial.println("Error\n\r\tISR time out error");
    break;
  case DHTLIB_ERROR_RESPONSE_TIMEOUT:
    Serial.println("Error\n\r\tResponse time out error");
    break;
  case DHTLIB_ERROR_DATA_TIMEOUT:
    Serial.println("Error\n\r\tData time out error");
    break;
  case DHTLIB_ERROR_ACQUIRING:
    Serial.println("Error\n\r\tAcquiring");
    break;
  case DHTLIB_ERROR_DELTA:
    Serial.println("Error\n\r\tDelta time to small");
    break;
  case DHTLIB_ERROR_NOTSTARTED:
    Serial.println("Error\n\r\tNot started");
    break;
  default:
    Serial.println("Unknown error");
    break;
  }
  Serial.print("Humidity (%): ");
  Serial.println(dht.getHumidity(), 2);

  Serial.print("Temperature (oC): ");
  Serial.println(dht.getCelsius(), 2);

  Serial.print("Temperature (oF): ");
  Serial.println(dht.getFahrenheit(), 2);

  Serial.print("Temperature (K): ");
  Serial.println(dht.getKelvin(), 2);

  Serial.print("Dew Point (oC): ");
  Serial.println(dht.getDewPoint());

  Serial.print("Dew Point Slow (oC): ");
  Serial.println(dht.getDewPointSlow());
}

boolean dhtRead()
{
  int result = dht.acquireAndWait(1000); // wait up to 1 sec (default indefinitely)

  if (result != DHTLIB_OK)
  {
    return false;
  }

  currentReading.temperature = dht.getFahrenheit();
  currentReading.humidity = dht.getHumidity();

  return true;
}

// Read sensor data and enqueue it
void readSensors()
{
  currentReading.brightness = analogRead(LDRPIN);
  currentReading.time = Time.now();

  // Get temperature data
  if (!dhtRead())
  {
#ifdef LOGGING
    Serial.println("Error reading from DHT!");
#endif
    return;
  }

  // Remove the oldest entry if the queue is full
  if (messageQueue.size() >= QUEUE_MAX_CAPACITY)
  {
    messageQueue.pop_back();
  }

  // Enqueue data point onto queue
  messageQueue.push_back(currentReading);
}

// Attempt to send all data points in the queue to the server as JSON objects
void publishData()
{
  // Consume queue
  while (messageQueue.size() > 0)
  {
    // Get data point at front of queue
    ReadingPayload front = messageQueue.front();

    // Format data into JSON
    snprintf(jsonBuffer, sizeof(jsonBuffer), "{\"tempF\":%1.2f,\"humidity\":%1.2f,\"brightness\":%lu,\"time\":%ld,\"id\":\"%s\"}",
             front.temperature, front.humidity, front.brightness, front.time, deviceID);

    // Ensure WiFi and socket are still connected
    connectWifi();
    maintainSocket();

    // Counter for failed attempts
    uint32_t failedPublishes = 0;

    // Attempt to send JSON to socket
    size_t bytesWritten = client.write(jsonBuffer);
    int error = client.getWriteError();

    // Retry publish if write failed
    if (error != ERR_OK)
    {
#ifdef LOGGING
      Serial.printlnf("Failed to send payload! Number of bytes written: %u", bytesWritten);
      Serial.println("Retrying...");
#endif
      // Retry up to 3 times
      while (failedPublishes++ < PUBLISH_RETRIES && error != ERR_OK)
      {
        connectWifi();
        maintainSocket();
        bytesWritten = client.write(jsonBuffer);
        error = client.getWriteError();
      }
    }

    // Dequeue data point if the publish was successful, otherwise return from this function
    if (error == ERR_OK)
    {
      messageQueue.pop_front();
      client.stop();
    }
    else
    {
      return;
    }
  }
}
