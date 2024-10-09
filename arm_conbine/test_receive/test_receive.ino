const int LED_PIN = 12; // 定義 LED 引腳
bool ledState = false; // LED 狀態變數

void setup() {
  Serial.begin(9600); // 初始化串行通訊
  pinMode(LED_PIN, OUTPUT); // 設定 LED 引腳為輸出
}

void loop() {
  if (Serial.available() > 0) { // 檢查是否有數據可讀
    char received = Serial.read(); // 讀取接收到的數據

    if (received == '1') {
      if (!ledState) { // 如果 LED 尚未點亮
        Serial.println("Signal received! Executing action...");
        digitalWrite(LED_PIN, HIGH); // 點亮 LED
        ledState = true; // 更新狀態為點亮
      }
    } else {
      if (ledState) { // 如果 LED 目前是點亮的狀態
        digitalWrite(LED_PIN, LOW); // 關閉 LED
        ledState = false; // 更新狀態為關閉
      }
    }
  }
}
