#include "Car.h"

Car::Car(Motor& fl, Motor& fr, Motor& rl, Motor& rr)
  : rearLeft(fl), frontLeft(fr), rearRight(rl), frontRight(rr) {}

void Car::begin() {
  frontLeft.begin();
  frontRight.begin();
  rearLeft.begin();
  rearRight.begin();
}

void Car::moveForward(int speed) {
  frontLeft.forward(speed);
  frontRight.forward(speed);
  rearLeft.forward(speed);
  rearRight.forward(speed);
}

void Car::moveBackward(int speed) {
  frontLeft.backward(speed);
  frontRight.backward(speed);
  rearLeft.backward(speed);
  rearRight.backward(speed);
}

void Car::turnRight(int speed) {
  frontLeft.backward(0);
  frontRight.forward(0);
  rearLeft.forward(speed);
  rearRight.backward(speed);
}

void Car::turnLeft(int speed) {
  frontLeft.forward(0);
  frontRight.backward(0);
  rearLeft.backward(speed);
  rearRight.forward(speed);
}

void Car::stop() {
  frontLeft.stop();
  frontRight.stop();
  rearLeft.stop();
  rearRight.stop();
}