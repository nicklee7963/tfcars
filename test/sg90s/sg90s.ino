#include <Servo.h>  // 包含Servo库

Servo myServo;  // 创建一个Servo对象

void setup() {
  myServo.attach(9);  // 将舵机连接到数字引脚9
}

void loop() {
  myServo.write(180);  // 将舵机转到0度
  delay(1000);  // 等待1秒
  
  
}
