#include <Adafruit_NeoPixel.h>

// Define the pin where the LED strip is connected
#define LED_PIN     4  // Pin to control the LED strip (DIN)

// Define the number of LEDs in the strip
#define NUM_LEDS    60  // Adjust according to your strip length

// Create a NeoPixel object
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();          // Initialize the NeoPixel strip
  strip.show();           // Initialize all pixels to 'off'
}

void loop() {
  // Test sequence: cycle through colors
  colorWipe(strip.Color(255, 0, 0), 50); // Red
  colorWipe(strip.Color(0, 255, 0), 50); // Green
  colorWipe(strip.Color(0, 0, 255), 50); // Blue
  rainbowCycle(20);                       // Rainbow effect
}

// Function to fill the strip with a single color, one LED at a time
void colorWipe(uint32_t color, int wait) {
  for (int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, color);   // Set the color for each pixel
    strip.show();                    // Update the strip to display the color
    delay(wait);                     // Wait between pixel updates
  }
}

// Function for a rainbow effect across the entire strip
void rainbowCycle(int wait) {
  uint16_t i, j;

  for (j = 0; j < 256 * 5; j++) { // 5 cycles of all colors on the wheel
    for (i = 0; i < strip.numPixels(); i++) {
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
