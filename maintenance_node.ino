/*
  ESP32 IoT Predictive Maintenance - Hardware Template

  Starter firmware only. Replace the placeholder sensor-reading
  functions after selecting and calibrating the actual sensors.
*/

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include "config.h"
#include "secrets.h"

WiFiClient espClient;
PubSubClient mqttClient(espClient);
unsigned long lastTelemetry = 0;

void connectWiFi() {
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Wi-Fi connected.");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Wi-Fi connection failed.");
  }
}

void connectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Connecting to MQTT...");

    if (mqttClient.connect(DEVICE_ID)) {
      Serial.println("connected.");
    } else {
      Serial.print("failed, state=");
      Serial.println(mqttClient.state());
      delay(2000);
    }
  }
}

// Replace these with real sensor-specific code.
float readTemperature() { return 25.0; }
float readVibration() { return 0.0; }
float readCurrent() { return 0.0; }
float readRPM() { return 0.0; }

void publishTelemetry() {
  float temperature = readTemperature();
  float vibration = readVibration();
  float current = readCurrent();
  float rpm = readRPM();

  char payload[256];

  snprintf(
    payload, sizeof(payload),
    "{\"device_id\":\"%s\",\"temperature\":%.2f,"
    "\"vibration\":%.2f,\"current\":%.2f,\"rpm\":%.2f}",
    DEVICE_ID, temperature, vibration, current, rpm
  );

  Serial.print("Publishing: ");
  Serial.println(payload);

  if (mqttClient.publish(MQTT_TOPIC, payload)) {
    Serial.println("MQTT publish successful.");
  } else {
    Serial.println("MQTT publish failed.");
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(VIBRATION_PIN, INPUT);
  pinMode(CURRENT_PIN, INPUT);
  pinMode(RPM_PIN, INPUT);

  connectWiFi();
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();
  if (!mqttClient.connected()) connectMQTT();

  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastTelemetry >= TELEMETRY_INTERVAL_MS) {
    lastTelemetry = now;
    publishTelemetry();
  }
}
