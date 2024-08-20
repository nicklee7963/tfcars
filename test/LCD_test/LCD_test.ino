#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// 設定 LCD 的 I2C 位址（通常為 0x27 或 0x3F）
LiquidCrystal_I2C lcd(0x27, 16, 2);  // 16x2 LCD, I2C address 0x27

void setup() {
  lcd.init();                      // 初始化 LCD
  lcd.backlight();                 // 開啟背光
  lcd.setCursor(0, 0);             // 將游標移到第一行第一列
  lcd.print("Hello");              // 顯示 "Hello"
}

void loop() {
  // 不需要在 loop 中執行任何操作
}
