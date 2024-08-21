#include "HX711.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// 电路设置
const int DT_PIN = 7;  // 数据引脚
const int SCK_PIN = 6; // 时钟引脚
const int scale_factor = 732;  // 校准因子，需根据具体情况调整
HX711 scale;
LiquidCrystal_I2C lcd(0x27, 16, 2);  // I2C 地址 0x27，16x2 LCD

void setup() {
    lcd.init();  // 初始化LCD
    lcd.backlight();  // 打开背光
    Serial.begin(9600);  // 初始化串口通讯
    scale.begin(DT_PIN, SCK_PIN);  // 初始化HX711
    scale.set_scale(scale_factor);  // 设置校准因子
    scale.tare();  // 重置秤以保证初始状态为0
}

void loop() {
    int weight = scale.get_units(10);  // 读取重量，平均10次测量以增加精度
    if (weight < 0) {
        weight = 0;  // 如果读数为负，设为0
    }
    Serial.println(weight, 0);  // 在串口监视器中显示重量
    String weightStr = String(weight) + " g";  // 将重量转换为字符串形式

    // 在LCD上显示重量
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Weight:");
    lcd.setCursor(0, 1);
    lcd.print(weightStr);

    delay(500);  // 每0.5秒更新一次显示
}
