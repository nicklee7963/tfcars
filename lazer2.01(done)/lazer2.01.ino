void setup() {
  Serial.begin(9600);       // 設置串口通信速率
  pinMode(40, OUTPUT);      // 設置 40 針腳為輸出
}

void loop() {
  if (Serial.available()) { // 檢查是否有串口數據可讀取
    char command = Serial.read(); // 讀取一個字節的數據
    if (command == 'H') {         // 如果接收到 'H'，打開雷射模組
      digitalWrite(40, HIGH);
    } else {  // 如果接收到 'L'，關閉雷射模組
      digitalWrite(40, LOW);
    }
  }
}