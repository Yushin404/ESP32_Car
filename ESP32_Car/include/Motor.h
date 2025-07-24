#ifndef MOTOR_H
#define MOTOR_H

class Motor {
private:
  int in1, in2, pwmPin, pwmChannel;

public:
  Motor(int in1, int in2, int pwmPin, int pwmChannel);
  void begin();
  void forward(int speed);
  void backward(int speed);
  void stop();
};

#endif