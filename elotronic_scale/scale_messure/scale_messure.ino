#include "HX711.h"

const int DT_PIN = 7;
const int SCK_PIN = 6;

const int scale_factor = 732;

HX711 scale;

void setup()
{
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
    Serial.println(scale.get_units(10),0);
    scale.power_down();
    delay(1000);
    scale.power_up();
}