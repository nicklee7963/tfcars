#include <Servo.h>

//Servo myServo0;
Servo myServo1;
Servo myServo2;
Servo myServo3;
Servo myServo4;
Servo myServo5;

void initial();
void before();
void after();
void after_after();
//void spin(int speed);
void grip(int grip);
void moveServoGradually(Servo servo, int startPos, int endPos, int stepDelay);

void setup(){
    //myServo0.attach(3);
    myServo1.attach(5);
    myServo2.attach(6);
    myServo3.attach(9);
    myServo4.attach(10);
    myServo5.attach(11);
}

void initial(){
    //spin(90);
    moveServoGradually(myServo4, myServo4.read(), 0, 20);
    moveServoGradually(myServo3, myServo3.read(), 0, 20);
    moveServoGradually(myServo2, myServo2.read(), 0, 20);
    moveServoGradually(myServo1, myServo1.read(), 0, 20);
}

void after_after(){
    //spin(90);
    moveServoGradually(myServo3, myServo3.read(), 0, 20);
    moveServoGradually(myServo2, myServo2.read(), 0, 20);
    moveServoGradually(myServo4, myServo4.read(), 0, 20);
    moveServoGradually(myServo1, myServo1.read(), 0, 20);
}

void before(){     
    //spin(90); 
    moveServoGradually(myServo4, myServo4.read(), 115, 20);
    moveServoGradually(myServo3, myServo3.read(), 40, 20);
    moveServoGradually(myServo2, myServo2.read(), 120, 20);
    moveServoGradually(myServo3, myServo3.read(), 115, 20);  // I make it smaller, avoiding hitting the table
    moveServoGradually(myServo2, myServo2.read(), 160, 20);
    moveServoGradually(myServo1, myServo1.read(), 0, 20);
}
/*
void before(){
    //spin(90); 
    moveServoGradually(myServo4, myServo4.read(), 125, 20);
    moveServoGradually(myServo2, myServo2.read(), 160, 20);
    moveServoGradually(myServo3, myServo3.read(), 115, 20);  // I make it smaller, avoiding hitting the table
    moveServoGradually(myServo1, myServo1.read(), 0, 20);
}
*/
void after(){
    //spin(90);
    moveServoGradually(myServo4, myServo4.read(), 180, 20);
    moveServoGradually(myServo3, myServo3.read(), 150, 20);  //180->160->150->140
    moveServoGradually(myServo2, myServo2.read(), 60, 20);   //90->80->60->55
    moveServoGradually(myServo1, myServo1.read(), 0, 20);
}

void before_after(){
    //spin(90);
    moveServoGradually(myServo4, myServo4.read(), 165, 20); //0->165
    moveServoGradually(myServo2, myServo2.read(), 95, 20);
    moveServoGradually(myServo3, myServo3.read(), 0, 20);
    
    moveServoGradually(myServo1, myServo1.read(), 0, 20);
}

void after_initial(){
    //spin(90);
    moveServoGradually(myServo4, myServo4.read(), 145, 20); //0->145
    moveServoGradually(myServo3, myServo3.read(), 0, 20);
    moveServoGradually(myServo2, myServo2.read(), 0, 20);
    moveServoGradually(myServo1, myServo1.read(), 0, 20);
}

/*void spin(int speed){
    myServo0.write(speed);
}*/

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
    grip(0); 
    // delay(3000);
    // initial();
    // delay(3000);
    // before();
    // //delay(3000);
    // grip(1);
    // before_after();
    // delay(3000);
    
    // after();
    // delay(3000);
    /*
    grip(0); 
    delay(3000);
    after_initial();
    delay(3000);
    */
    
    //after_after();
    /*after();
    grip(0);
    delay(3000);
    */
   initial();
}