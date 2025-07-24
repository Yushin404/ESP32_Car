#ifndef CAR_H
#define CAR_H

#include "Motor.h"

class Car {
private:
  Motor& frontLeft;
  Motor& frontRight;
  Motor& rearLeft;
  Motor& rearRight;

public:
  Car(Motor& fl, Motor& fr, Motor& rl, Motor& rr);
  void begin();
  void moveForward(int speed);
  void moveBackward(int speed);
  void turnLeft(int speed);
  void turnRight(int speed);
  void stop();
};

#endif