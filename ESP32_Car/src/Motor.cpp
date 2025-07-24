#include <Arduino.h>
#include "Motor.h"

Motor::Motor(int in1, int in2, int pwmPin, int pwmChannel)
  : in1(in1), in2(in2), pwmPin(pwmPin), pwmChannel(pwmChannel) {}

void Motor::begin() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  ledcSetup(pwmChannel, 5000, 8);
  ledcAttachPin(pwmPin, pwmChannel);
}

void Motor::forward(int speed) {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  ledcWrite(pwmChannel, speed);
}

void Motor::backward(int speed) {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  ledcWrite(pwmChannel, speed);
}

void Motor::stop() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  ledcWrite(pwmChannel, 0);
}