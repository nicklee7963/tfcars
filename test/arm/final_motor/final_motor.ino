#define servo0_pin 3
#define servo1_pin 5
#define servo2_pin 6
#define servo3_pin 9
#define servo4_pin 10
#define servo5_pin 11
#define gripper_open 180
#define gripper_close 100

# include <Servo.h>

// 創建一個伺服物件
Servo myServo0;
Servo myServo1;
Servo myServo2;
Servo myServo3;
Servo myServo4;
Servo myServo5;


const int initial_degree[6] = [ , , , , , ];
int current_degree[6] = [ , , , , , ];

void initial();

void setup() {
  // 將伺服馬達連接到Arduino的9號引腳
  myServo0.attach(servo0_pin);
  myServo1.attach(servo1_pin);
  myServo2.attach(servo2_pin);
  myServo3.attach(servo3_pin);
  myServo4.attach(servo4_pin);
  myServo5.attach(servo5_pin);

  initial();
  // 設置伺服馬達角度為90度
  
  
}


void initial(){
  myServo0.write(initial_degree[0]);
  myServo1.write(initial_degree[1]);
  myServo2.write(initial_degree[2]);
  myServo3.write(initial_degree[3]);
  myServo4.write(initial_degree[4]);
  myServo5.write(initial_degree[5]);
}



int slow_move(final, pin)
{
  for(;current_degree[pin] < final; current_degree[pin] += 5)
  {
    delay(10); 
  }

}
 
bool is_detected(){
  pass
}

void grip(){
  
}

void loop() {

  myServo0.write(current_degree[servo0_pin]);
  myServo1.write(current_degree[servo1_pin]);
  myServo2.write(current_degree[servo2_pin]);
  myServo3.write(current_degree[servo3_pin]);
  myServo4.write(current_degree[servo4_pin]);

 
}





