#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include "Motor.h"
#include "Car.h"

#define M1_IN1 12
#define M1_IN2 13
#define M1_PWM 14

#define M2_IN1 25
#define M2_IN2 26
#define M2_PWM 27

#define M3_IN1 33
#define M3_IN2 2
#define M3_PWM 0

#define M4_IN1 5
#define M4_IN2 15
#define M4_PWM 4

#define STBY_A 32
#define STBY_B 16

const char* ssid = "ESP32_CAR";
const char* password = "12345678";
WebServer server(80);

Motor motor1(M1_IN1, M1_IN2, M1_PWM, 0);
Motor motor2(M2_IN1, M2_IN2, M2_PWM, 1);
Motor motor3(M3_IN1, M3_IN2, M3_PWM, 2);
Motor motor4(M4_IN1, M4_IN2, M4_PWM, 3);
Car car(motor1, motor2, motor3, motor4);

String htmlPage = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <title>ESP32 Car</title>
</head>
<body>
  <h2>ESP32 Car</h2>
  <p>
    <button onclick="fetch('/forward')">Forward</button><br><br>
    <button onclick="fetch('/left')">Left</button>
    <button onclick="fetch('/right')">Right</button><br><br>
    <button onclick="fetch('/backward')">Backward</button><br><br>
    <button onclick="fetch('/stop')">Stop</button>
  </p>
</body>
</html>
)rawliteral";


void handleRoot()      { server.send(200, "text/html", htmlPage); }
void handleForward()   { car.moveForward(200); server.send(200, "text/plain", "Forward"); }
void handleBackward()  { car.moveBackward(200); server.send(200, "text/plain", "Backward"); }
void handleLeft()      { car.turnLeft(200); server.send(200, "text/plain", "Left"); }
void handleRight()     { car.turnRight(200); server.send(200, "text/plain", "Right"); }
void handleStop()      { car.stop(); server.send(200, "text/plain", "Stop"); }

void setup() {
  Serial.begin(115200);
  pinMode(STBY_A, OUTPUT);
  pinMode(STBY_B, OUTPUT);
  digitalWrite(STBY_A, HIGH);
  digitalWrite(STBY_B, HIGH);

  car.begin();

  WiFi.softAP(ssid, password);
  Serial.println("WiFi Started: connect to ESP32_CAR");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot);
  server.on("/forward", handleForward);
  server.on("/backward", handleBackward);
  server.on("/left", handleLeft);
  server.on("/right", handleRight);
  server.on("/stop", handleStop);
  server.begin();
}

void loop() {
  server.handleClient();
}
