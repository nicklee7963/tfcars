#include "HX711.h"
#include <Wire.h> // I2C程式庫
#include <LiquidCrystal_I2C.h> // LCD_I2C模組程式庫
const int DT_PIN = 7;
const int SCK_PIN = 6;
const int confidence = 2;
const int scale_factor = 725;
const int heavy = 64;  //blue
const int medium = 50;   //green
const int light = 33;   //red
int digitnum = 1;
int rer = 0;
HX711 scale;
LiquidCrystal_I2C lcd(0x27, 16, 2); 

int roundToInt(double value) {
    return (int)(value >= 0 ? value + 0.5 : value - 0.5);
}

int digit(int num){
  return (int(num/10) >= 1 ? 2:1);
}

void setup()
{ 
  
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0); 
  lcd.print("Loading");
  Serial.begin(9600);
  // Serial.println("Initializing the scale");

  scale.begin(DT_PIN, SCK_PIN);
  // Serial.println("Before setting up the scale");
  // Serial.println(scale.get_units(5), 0);
  scale.set_scale(scale_factor);
  scale.tare();

  // Serial.println("After setting up the scale");
  // Serial.println(scale.get_units(5), 0);

  // Serial.println("readings:");
  delay(1000);

}

void loop()
{
  
  
  int weight;
  
  lcd.setCursor(0, 0); 
  lcd.print("weight:");
  lcd.setCursor(0, 1);
  weight = roundToInt(scale.get_units(1));
  if(digitnum != digit(weight)){
    lcd.clear();
    digitnum = digit(weight);
  }
  if (weight<= heavy+5 && weight >= heavy-5){
    int success = 0;
    for(int i = 0; i < confidence; i++){
      weight = roundToInt(scale.get_units(1));
      if (weight<= heavy+5 && weight >= heavy-5){
        success++;

      }
      // Serial.println(success);
      delay(500);
    }
    if (success == confidence&&rer == 0){
      Serial.println("blue");
      rer = 1;
    }
    
  }
  else if (weight<= medium+5 && weight >= medium-5){
    int success = 0;
    for(int i = 0; i < confidence; i++){
      weight = roundToInt(scale.get_units(1));
      if (weight<= medium+5 && weight >= medium-5){
        success++;

      }
      // Serial.println(success);
      delay(500);
    }
    if (success == confidence&&rer == 0){
      Serial.println("green");
      rer = 1;
    }
    
  }
  else if (weight<= light+5 && weight >= light-5){
    int success = 0;
    for(int i = 0; i < confidence; i++){
      weight = roundToInt(scale.get_units(1));
      if (weight<= light+5 && weight >= light-5){
        success++;

      }
      // Serial.println(success);
      delay(500);
    }
    if (success == confidence&&rer == 0){
      Serial.println("red");
      rer = 1;
    }
    
  }
 
  String weightStr = String(weight) + " g";
  lcd.print(weightStr);
    


  scale.power_down();
  delay(10);
  scale.power_up();
    
}