/*
 * Project particle-client
 * Description: Send sensor data to a webserver with TCP
 * Author: Nathan Robinson
 * Date:
 */

// Header Files:
#include "Particle.h"
#include "Grove_Temperature_And_Humidity_Sensor.h"
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
#define DHTPIN D2
#define LDRPIN A0

// System configuration macros
SYSTEM_MODE(MANUAL);
SYSTEM_THREAD(ENABLED);

// Sensor Data Point Structure
struct ReadingPayload
{
  time_t time;        // Unix time
  float temperature;  // Farenheit (degrees)
  float humidity;     // Relative Humidity %
  uint8_t brightness; // Relative brightness 0-255
};

ReadingPayload currentReading;

// Global Objects
TCPClient client;
DHT dht(DHTPIN);
std::deque<ReadingPayload> messageQueue;
char jsonBuffer[400];

// Operational Parameters
const uint32_t readingPeriod = 5;  // Read every 5 seconds
const uint32_t publishPeriod = 30; // Publish every 30 seconds

// Socket settings
const char *serverAddress = "192.168.1.1";
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
  if (wifiConnected)
  {
    Serial.println("Established Wi-Fi connection.");
  }
  else
  {
    Serial.println("Failed to connect to Wi-Fi!");
  }
#endif
}

// Function prototypes
void readSensors();
void publishData();

// Software timers
Timer readTimer(readingPeriod *SECONDS_MS, readSensors);
Timer publishTimer(publishPeriod *SECONDS_MS, publishData);

// Initialize sensors and objects
void setup()
{
  // Start serial connection to PC
  Serial.begin(115200);

  // Initialize sensors
  pinMode(LDRPIN, INPUT);
  dht.begin();

  // Connect to WiFi
  connectWifi();

  // Connect to the server
  maintainSocket();

  // Start timers
  readTimer.start();
  publishTimer.start();
}

// Read sensor data and send it to the server
void loop()
{
}

// Read sensor data and enqueue it
void readSensors()
{
  // Save sensor reading to data point object
  currentReading.temperature = dht.getTempFarenheit();
  currentReading.humidity = dht.getHumidity();
  currentReading.brightness = analogRead(LDRPIN) >> 4;
  currentReading.time = Time.now();

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
    snprintf(jsonBuffer, sizeof(jsonBuffer), "{\"time\":%ld,\"tempF\":%1.2f,\"humidity\":%1.2f,\"brightness\":%u}",
             front.time, front.temperature, front.humidity, front.brightness);

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
      messageQueue.pop_front();
    else
      return;
  }
}
