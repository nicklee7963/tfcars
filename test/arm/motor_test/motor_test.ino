#include <Servo.h>

// 創建一個伺服物件
Servo myServo;

void setup() {
  // 將伺服馬達連接到Arduino的9號引腳
  myServo.attach(9);
  // 設置伺服馬達角度為90度
  
  myServo.write(0);
}

void loop() {
  // 在此例程中，我們不需要loop的內容
}
