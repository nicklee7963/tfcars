#include "HX711.h"

const int DT_PIN = 7;
const int SCK_PIN = 6;
const int sample_weight = 62;

HX711 scale;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  scale.begin(DT_PIN, SCK_PIN);
  scale.set_scale();
  scale.tare();
  Serial.println("Nothing on it");
  Serial.println(scale.get_units(10));
  Serial.println("please put sample");
}

void loop() {
  // put your main code here, to run repeatedly:
  float current_weight = scale.get_units(10);
  float scale_factor = (current_weight/sample_weight);
  Serial.println("Scale number:");
  Serial.println(scale_factor,0);

}
