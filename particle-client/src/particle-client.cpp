/*
 * Project particle-client
 * Description: Send sensor data to a webserver with TCP
 * Author: Nathan Robinson
 * Date:
 */

// System configuration macros
SYSTEM_MODE(MANUAL);
SYSTEM_THREAD(ENABLED);

// Global Objects
TCPClient client;

// Initialize sensors and objects
void setup()
{

  WiFi.connect();
}

// Read sensor data and send it to the server
void loop()
{
}
