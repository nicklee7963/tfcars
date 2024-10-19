const int hallPin = 2; // Pin connected to the Hall sensor

void setup() {
  pinMode(hallPin, INPUT);  // Set pin 2 as input
  Serial.begin(115200);       // Start the serial communication
}

void loop() {
  int sensorState = digitalRead(hallPin);  // Read the sensor state
  
  // When the Hall sensor detects a magnet, it outputs LOW (0)
  if (sensorState == LOW) {
    Serial.println(1);  // Magnet is near
  } else {
    Serial.println(0);  // Magnet is away
  }
  
  delay(100);  // Add a small delay to avoid flooding the serial output
}
