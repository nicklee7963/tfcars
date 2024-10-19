#include <Adafruit_NeoPixel.h>
//#include <Servo.h>

// 定義燈條相關參數
#define LED_PIN 4      // 燈條的資料輸入腳位
#define NUM_LEDS 60    // 燈條上 LED 的數量
#define HALL_SENSOR_PIN 2  // 霍爾效應傳感器引腳


// 定義其他引腳
int laserPin = 7;      // 雷射光
int hallSensorValue;   // 存儲霍爾效應傳感器的狀態
int laserPin_mea = 3;     // 雷射光

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);
//Servo armServo;  // 舵機，用於控制手臂

void setup() {
  // 初始化串口
  Serial.begin(9600);

  // 初始化燈條
  strip.begin();
  strip.show();  // 初始化燈條關閉

  // 設置霍爾效應傳感器和雷射引腳模式
  pinMode(HALL_SENSOR_PIN, INPUT);
  pinMode(laserPin, OUTPUT);
  pinMode(laserPin_mea, OUTPUT);
  digitalWrite(laserPin_mea, HIGH);
  
  /*
  // 初始化舵機
  armServo.attach(11);  // 連接舵機到11號引腳
  armServo.write(0);   // 恢復到初始位置
  */
}

void loop() {
  hallSensorValue = digitalRead(HALL_SENSOR_PIN);

  if (hallSensorValue == LOW) {
    // 當霍爾效應傳感器檢測到磁鐵時，顯示漸變顏色
    rainbowCycle(20);
  } else {
    // 當磁鐵移除時，關閉所有燈條
    turnOffAllLEDs();
    
    // 檢查是否有串口數據可讀
    if (Serial.available() > 0) {
      char command = Serial.read();  // 讀取單個字元
    /*
      // 控制燈條顏色（模擬前後輪 LED 運動）
      if (command == 'F') {  // 'F' 表示前進 (顯示白色燈)
        setStripColor(strip.Color(255, 255, 255), 3000);  // 白色
      } else if (command == 'S') {  // 'S' 表示停止 (關閉燈條)
        setStripColor(strip.Color(0, 0, 0), 0);  // 關閉燈條
      }
    */
      
      // 控制綠色 LED 燈
      if (command == 'G') {  // 'G' 表示綠燈亮起
        setStripColor(strip.Color(0, 255, 0), 2000);  // 綠色
      }

      // 控制紅色 LED 燈
      if (command == 'R') {  // 'R' 表示紅燈亮起
        setStripColor(strip.Color(255, 0, 0), 2000);  // 紅色
      }

      // 控制黃色 LED 燈
      if (command == 'Y') {  // 'Y' 表示黃燈亮起
        setStripColor(strip.Color(255, 50, 0), 2000);  // 黃色
      }
    /*
      // 控制手臂的舵機（模擬夾取動作）
      if (command == 'p') {  // 'P' 表示夾取病雞
        armServo.write(90);  // 旋轉舵機到90度，模擬夾取
        delay(1000);         // 保持1秒
        armServo.write(0);   // 恢復到初始位置
      }
    */
      // 控制雷射光
      if (command == 'L') {  // 'L' 表示發射雷射
        digitalWrite(laserPin, HIGH);
        setStripColor(strip.Color(255, 0, 0), 3500);  // 紅色

        digitalWrite(laserPin, LOW);
      }
    }
  }
}

// 函數：設定燈條顏色並保持亮起一定時間
void setStripColor(uint32_t color, int duration) {
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();  // 更新燈條顯示

  if (duration > 0) {
    delay(duration);  // 保持燈條亮起指定的時間
    // 關閉燈條
    turnOffAllLEDs();
  }
}



// 函數：關閉所有 LED


// Function for a rainbow effect across the entire strip
void rainbowCycle(int wait) {
  uint16_t i, j;

  for (j = 0; j < 256 * 5; j++) { // 5 cycles of all colors on the wheel
    for (i = 0; i < strip.numPixels(); i++) {
      if (digitalRead(HALL_SENSOR_PIN) == HIGH) {
        turnOffAllLEDs();  // 偵測到磁鐵移除，關閉燈條
        return;
      }
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Helper function to generate rainbow colors across 0-255 positions
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if (WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else if (WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  } else {
    WheelPos -= 170;
    return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  }
}
void turnOffAllLEDs() {
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0));  // 關閉所有燈
  }
  strip.show();  // 更新燈條顯示
}#include <Adafruit_NeoPixel.h>
//#include <Servo.h>

// 定義燈條相關參數
#define LED_PIN 4      // 燈條的資料輸入腳位
#define NUM_LEDS 60    // 燈條上 LED 的數量
#define HALL_SENSOR_PIN 2  // 霍爾效應傳感器引腳


// 定義其他引腳
int laserPin = 7;      // 雷射光
int hallSensorValue;   // 存儲霍爾效應傳感器的狀態
int laserPin_mea = 3;     // 雷射光

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);
//Servo armServo;  // 舵機，用於控制手臂

void setup() {
  // 初始化串口
  Serial.begin(9600);

  // 初始化燈條
  strip.begin();
  strip.show();  // 初始化燈條關閉

  // 設置霍爾效應傳感器和雷射引腳模式
  pinMode(HALL_SENSOR_PIN, INPUT);
  pinMode(laserPin, OUTPUT);
  pinMode(laserPin_mea, OUTPUT);
  digitalWrite(laserPin_mea, HIGH);
  
  /*
  // 初始化舵機
  armServo.attach(11);  // 連接舵機到11號引腳
  armServo.write(0);   // 恢復到初始位置
  */
}

void loop() {
  hallSensorValue = digitalRead(HALL_SENSOR_PIN);

  if (hallSensorValue == LOW) {
    // 當霍爾效應傳感器檢測到磁鐵時，顯示漸變顏色
    rainbowCycle(20);
  } else {
    // 當磁鐵移除時，關閉所有燈條
    turnOffAllLEDs();
    
    // 檢查是否有串口數據可讀
    if (Serial.available() > 0) {
      char command = Serial.read();  // 讀取單個字元
    /*
      // 控制燈條顏色（模擬前後輪 LED 運動）
      if (command == 'F') {  // 'F' 表示前進 (顯示白色燈)
        setStripColor(strip.Color(255, 255, 255), 3000);  // 白色
      } else if (command == 'S') {  // 'S' 表示停止 (關閉燈條)
        setStripColor(strip.Color(0, 0, 0), 0);  // 關閉燈條
      }
    */
      
      // 控制綠色 LED 燈
      if (command == 'G') {  // 'G' 表示綠燈亮起
        setStripColor(strip.Color(0, 255, 0), 2000);  // 綠色
      }

      // 控制紅色 LED 燈
      if (command == 'R') {  // 'R' 表示紅燈亮起
        setStripColor(strip.Color(255, 0, 0), 2000);  // 紅色
      }

      // 控制黃色 LED 燈
      if (command == 'Y') {  // 'Y' 表示黃燈亮起
        setStripColor(strip.Color(255, 50, 0), 2000);  // 黃色
      }
    /*
      // 控制手臂的舵機（模擬夾取動作）
      if (command == 'p') {  // 'P' 表示夾取病雞
        armServo.write(90);  // 旋轉舵機到90度，模擬夾取
        delay(1000);         // 保持1秒
        armServo.write(0);   // 恢復到初始位置
      }
    */
      // 控制雷射光
      if (command == 'L') {  // 'L' 表示發射雷射
        digitalWrite(laserPin, HIGH);
        setStripColor(strip.Color(255, 0, 0), 3500);  // 紅色

        digitalWrite(laserPin, LOW);
      }
    }
  }
}

// 函數：設定燈條顏色並保持亮起一定時間
void setStripColor(uint32_t color, int duration) {
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();  // 更新燈條顯示

  if (duration > 0) {
    delay(duration);  // 保持燈條亮起指定的時間
    // 關閉燈條
    turnOffAllLEDs();
  }
}



// 函數：關閉所有 LED


// Function for a rainbow effect across the entire strip
void rainbowCycle(int wait) {
  uint16_t i, j;

  for (j = 0; j < 256 * 5; j++) { // 5 cycles of all colors on the wheel
    for (i = 0; i < strip.numPixels(); i++) {
      if (digitalRead(HALL_SENSOR_PIN) == HIGH) {
        turnOffAllLEDs();  // 偵測到磁鐵移除，關閉燈條
        return;
      }
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Helper function to generate rainbow colors across 0-255 positions
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if (WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else if (WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  } else {
    WheelPos -= 170;
    return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  }
}
void turnOffAllLEDs() {
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0));  // 關閉所有燈
  }
  strip.show();  // 更新燈條顯示
}