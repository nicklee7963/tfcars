






#include "HX711.h"
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
const int DT_PIN = 7;
const int SCK_PIN = 6;

const int scale_factor = 732;

HX711 scale;


#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);




void setup()
{
    display.begin(SSD1306_SWITCHCAPVCC,0x3C);
    display.clearDisplay();
    Serial.begin(9600);
    Serial.println("Initializing the scale");

    scale.begin(DT_PIN, SCK_PIN);
    scale.set_scale(scale_factor);
    scale.tare();

    Serial.println("Before setting up the scale");

    Serial.println("readings:");


}

void loop()
{

    
    
    
    int weight = scale.get_units(10);
    
    Serial.println(weight,0);
    String weightStr = String(weight) + " g";
    
    display.clearDisplay();
    display.setTextSize(2);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0,0);
    display.println("Weight: ");
    display.setCursor(30,17);
    display.println(weightStr);
    display.display();


    scale.power_down();
    delay(100);
    scale.power_up();
    
}