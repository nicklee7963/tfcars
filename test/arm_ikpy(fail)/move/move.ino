#include <Servo.h>

Servo servo1;  // 控制第一個伺服馬達
Servo servo2;  // 控制第二個伺服馬達
Servo servo3;  // 控制第三個伺服馬達

void setup() {
  Serial.begin(9600);  // 設置串口通信速率
  servo1.attach(9);    // 將伺服馬達連接到Arduino的9號腳位
  servo2.attach(10);   // 將伺服馬達連接到Arduino的10號腳位
  servo3.attach(11);   // 將伺服馬達連接到Arduino的11號腳位
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    int separator1 = input.indexOf(':');
    int separator2 = input.indexOf(':', separator1 + 1);

    if (separator1 > 0 && separator2 > separator1) {
      int servoNumber = input.substring(0, separator1).toInt();
      int angle = input.substring(separator1 + 1).toInt();

      // 設定對應伺服馬達的角度
      switch (servoNumber) {
        case 1:
          servo1.write(angle);
          break;
        case 2:
          servo2.write(angle);
          break;
        case 3:
          servo3.write(angle);
          break;
        default:
          Serial.println("Invalid servo number.");
          break;
      }
    }
  }
}
