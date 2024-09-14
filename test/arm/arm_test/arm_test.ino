#include <Servo.h>

Servo myServo0;
Servo myServo1;
Servo myServo2;
Servo myServo3;
Servo myServo4;
Servo myServo5;


void initial();
void before();
void after();
void after_after();
void spin(int speed);
void grip(int grip);

void setup(){
    myServo0.attach(3);
    myServo1.attach(5);
    myServo2.attach(6);
    myServo3.attach(9);
    myServo4.attach(10);
    myServo5.attach(11);
}
void initial(){
    spin(90);
    myServo4.write(0);
    myServo3.write(0);
    myServo2.write(0);
    myServo1.write(0);
}

void after_after(){
    spin(90);
    myServo3.write(0);
    myServo2.write(0);
    myServo4.write(0);
    myServo1.write(0);
}
void before(){
    spin(90);
    myServo2.write(160);
    myServo3.write(95);
    myServo4.write(125);
    myServo1.write(0);

}

void after(){
    spin(90);
    myServo4.write(180);
    myServo3.write(180);
    myServo2.write(60);
    myServo1.write(0);
}

void spin(int speed){
    myServo0.write(speed);
}

void grip(int grip){
    if (grip == 1){
        myServo5.write(100);
    }
    else if (grip == 0){
        myServo5.write(180);
    }
}

void loop(){
    grip(0); 
    delay(3000);
    initial();
    delay(3000);
    before();
    delay(3000);
    grip(1);
    delaf(3000);
    after();
    delay(3000);
    grip(0);
    delay(3000);
    after_after();
    
    




}