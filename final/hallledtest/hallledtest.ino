#include <Adafruit_NeoPixel.h>

#define HALL_SENSOR_PIN 2
#define LED_PIN 4
#define NUM_LEDS 60  // 根據您的 WS2812 燈條的 LED 數量進行調整

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pinMode(HALL_SENSOR_PIN, INPUT);
  strip.begin();
  strip.show();  // 初始化所有像素關閉
}

void loop() {
  int hallSensorValue = digitalRead(HALL_SENSOR_PIN);

  if (hallSensorValue == LOW) {  // 當磁鐵靠近時，霍爾效應傳感器輸出低電平
    for (int i = 0; i < 256; i+=50) {
        for(int k = 0; k < NUM_LEDS; k++) {
            if(digitalRead(HALL_SENSOR_PIN)){
                break;
            }
            strip.setPixelColor(k, strip.Color(255 - i, i , 0));  // 亮起紅色燈
            strip.show();
            delay(50);
        }
        if(digitalRead(HALL_SENSOR_PIN)){
                break;
            }
        
        
    }
    
    for(int i = 0; i < 256; i+=50) {
        for(int k = 0; k < NUM_LEDS; k++) {
            strip.setPixelColor(k, strip.Color(0, 255 - i , i));  // 亮起綠色燈
            if(digitalRead(HALL_SENSOR_PIN)){
                break;
            }
            strip.show();
            delay(50);  // 加一點延遲來顯示顏色變化
        }
        if(digitalRead(HALL_SENSOR_PIN)){
                break;
            }
    }
    for(int i = 0; i < 256; i+=50) {
        for(int k = 0; k < NUM_LEDS; k++) {
            strip.setPixelColor(k, strip.Color(i, 0 , 255 - i));  // 亮起藍色燈
            if(digitalRead(HALL_SENSOR_PIN)){
                break;
            }
            strip.show();
            delay(50);  // 加一點延遲來顯示顏色變化
        }
        if(digitalRead(HALL_SENSOR_PIN)){
                break;
            }
        
    }

    hallSensorValue = digitalRead(HALL_SENSOR_PIN);  // 更新霍爾效應傳感器的狀態
  }

  // 磁鐵離開時關閉所有燈
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0));  // 關閉所有燈
  }
  strip.show();
  delay(10);  // 加一點延遲避免頻繁刷新
}
