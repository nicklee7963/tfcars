#include <Servo.h>
bool completea = 0;
bool completeb = 0;
Servo myServo0;
Servo myServo1;
Servo myServo2;
Servo myServo3;
Servo myServo4;
Servo myServo5;

void after_before();
void before_before();
void before();
void goose();
//void spin(int speed);
void grip(int grip);
void moveServoGradually(Servo servo, int startPos, int endPos, int stepDelay);
void chicken(){
  moveServoGradually(myServo3, myServo3.read(), 20, 20);
  moveServoGradually(myServo4, myServo4.read(), 100, 20);
  myServo5.write(180);
  moveServoGradually(myServo0, myServo0.read(), 95, 20);
  
  before();
  delay(1000);
  myServo5.write(80);
  delay(500);
  after_before();
  delay(1000);
  moveServoGradually(myServo0, myServo0.read(), 0, 20);
  
  delay(1000);
  myServo4.write(0);
  myServo3.write(0);
  delay(500);
  
}
void goose(){
    moveServoGradually(myServo4, myServo4.read(), 10, 20);
  moveServoGradually(myServo2, myServo2.read(), 60, 20);
  delay(500);
  myServo5.write(80);
  delay(500);
  moveServoGradually(myServo2, myServo2.read(), 0, 20);
  delay(500);
  moveServoGradually(myServo3, myServo3.read(), 20, 20);
  
  moveServoGradually(myServo0, myServo0.read(), 100, 20);
  delay(500);
  before();
  delay(500);
  myServo5.write(180);
  delay(500);
  after_before();
  delay(500);

  moveServoGradually(myServo0, myServo0.read(), 0, 20);
  delay(500);
}
void setup(){
    Serial.begin(9600);
    myServo0.attach(3);
    myServo1.attach(5);
    myServo2.attach(6);
    myServo3.attach(9);
    myServo4.attach(10);
    myServo5.attach(11);
}
void initial_setup(){
    myServo0.write(0);
    myServo1.write(0);
    myServo2.write(0);
    myServo3.write(0);
    myServo4.write(20);
    myServo5.write(80);


}
void after_before(){
    //spin(90);    
    moveServoGradually(myServo4, myServo4.read(), 20, 20);
    moveServoGradually(myServo2, myServo2.read(), 100, 20); //160

    
    moveServoGradually(myServo3, myServo3.read(), 50, 20); //115

    moveServoGradually(myServo2, myServo2.read(), 0, 20);
    moveServoGradually(myServo3, myServo3.read(), 20, 20);
    // moveServoGradually(myServo2, myServo2.read(), 80, 20);
    // moveServoGradually(myServo3, myServo3.read(), 50, 20);
    // moveServoGradually(myServo2, myServo2.read(), 50, 20);
    // moveServoGradually(myServo3, myServo3.read(), 30, 20);
    // moveServoGradually(myServo2, myServo2.read(), 0, 20);
    // moveServoGradually(myServo3, myServo3.read(), 20, 20);
    moveServoGradually(myServo1, myServo1.read(), 0, 20);
}



void before(){     
    //spin(90); 
    // moveServoGradually(myServo4, myServo4.read(), 115, 20);
    // moveServoGradually(myServo3, myServo3.read(), 40, 20);
    // moveServoGradually(myServo2, myServo2.read(), 120, 20);
    // moveServoGradually(myServo3, myServo3.read(), 115, 20);  // I make it smaller, avoiding hitting the table
    // moveServoGradually(myServo2, myServo2.read(), 160, 20);
    // moveServoGradually(myServo1, myServo1.read(), 0, 20);
    moveServoGradually(myServo4, myServo4.read(), 150, 20);
    moveServoGradually(myServo2, myServo2.read(), 60, 20);
    moveServoGradually(myServo3, myServo3.read(), 40, 20);

    moveServoGradually(myServo2, myServo2.read(), 100, 20);
    moveServoGradually(myServo3, myServo3.read(), 80, 20);
    moveServoGradually(myServo2, myServo2.read(), 140, 20);
    moveServoGradually(myServo3, myServo3.read(), 125, 20);
    moveServoGradually(myServo2, myServo2.read(), 160, 20);
    moveServoGradually(myServo1, myServo1.read(), 0, 20);
    

}



void grip(int grip){
    if (grip == 1){
        moveServoGradually(myServo5, myServo5.read(), 100, 20);
    }
    else if (grip == 0){
        moveServoGradually(myServo5, myServo5.read(), 180, 20);
    }
}

// 讓伺服馬達一點一點移動的函數
void moveServoGradually(Servo servo, int startPos, int endPos, int stepDelay){
    if (startPos < endPos) {
        for (int pos = startPos; pos <= endPos; pos++) {
            servo.write(pos);
            delay(stepDelay);
        }
    } else {
        for (int pos = startPos; pos >= endPos; pos--) {
            servo.write(pos);
            delay(stepDelay);
        }
    }
}

void loop(){
  
  initial_setup();
  
  if (Serial.available() > 0) { // 檢查是否有數據可讀
    char received = Serial.read(); // 讀取接收到的數據

    if (received == 'P'&&completea == 0) {
        completea = 1;
        goose();
    }
    if (received == 'p'&&completeb == 0){
        completeb =1;
        chicken();
    }
  }
  
  
  

  
//   moveServoGradually(myServo0, myServo0.read(), 90, 20);
//   moveServoGradually(myServo0, myServo0.read(), 90, 20);
//   moveServoGradually(myServo0, myServo0.read(), 90, 20);
//   moveServoGradually(myServo0, myServo0.read(), 90, 20);
//   moveServoGradually(myServo0, myServo0.read(), 90, 20);
//   moveServoGradually(myServo0, myServo0.read(), 90, 20);


}