#include "HX711.h"
const int DT_PIN = 7;
const int SCK_PIN = 6;

const int scale_factor = -12;

HX711 scale;


void setup()
{
    Serial.begin(115200);
    Serial.println("Initializing the scale");

    scale.begin(DT_PIN, SCK_PIN);
    Serial.println("Before setting up the scale");
    Serial.println(scale.get_units(5), 0);
    scale.set_scale(scale_factor);
    scale.tare();

    Serial.println("After setting up the scale");
    Serial.println(scale.get_units(5), 0);

    Serial.println("readings:");


}

void loop()
{

    
    
    
   Serial.println(scale.get_units(10), 0);
    // String weightStr = String(weight) + " g";
    
    // display.clearDisplay();
    // display.setTextSize(2);
    // display.setTextColor(SSD1306_WHITE);
    // display.setCursor(0,0);
    // display.println("Weight: ");
    // display.setCursor(30,17);
    // display.println(weightStr);
    // display.display();


    scale.power_down();
    delay(100);
    scale.power_up();
    
}