#define DIR_PIN 2
#define STEP_PIN 3

void setup() {
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  digitalWrite(DIR_PIN, HIGH);  // 設置方向
}

void loop() {
  digitalWrite(STEP_PIN, HIGH);
  delayMicroseconds(1000);  // 調整這個延遲來改變步進速度
  digitalWrite(STEP_PIN, LOW);
  delayMicroseconds(1000);
}
