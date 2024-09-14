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


const int initial_degree[6] = [0 ,135 ,130 ,0 ,0 ,gripper_open ];
int current_degree[6];
const int before_degree[6] = [0,45,70,80,160,gripper_open];
const int after_degree[6] = [0,135,60,10,160,gripper_open];
void initial();

void current(int move[6]; current_degree){
  current_degree = move;
}

void setup() {
  // 將伺服馬達連接到Arduino的9號引腳
  myServo0.attach(servo0_pin);
  myServo1.attach(servo1_pin);
  myServo2.attach(servo2_pin);
  myServo3.attach(servo3_pin);
  myServo4.attach(servo4_pin);
  myServo5.attach(servo5_pin);

  initial();
  
  
  
}


void initial(){
  myServo0.write(initial_degree[0]);
  myServo1.write(initial_degree[1]);
  myServo2.write(initial_degree[2]);
  myServo3.write(initial_degree[3]);
  myServo4.write(initial_degree[4]);
  myServo5.write(initial_degree[5]);
  current(initial_degree);
}



int slow_move(int move[6])
{
  for(int i = 1; i < 5; i++){
    int gap = move[i] - current_degree[i];
    
  }
  

}
 
bool is_detected(){
  pass;
}

void grip(){
  myServo5.write(gripper_close);
  
}

void loop() {

  
  myServo1.write(current_degree[servo1_pin]);
  myServo2.write(current_degree[servo2_pin]);
  myServo3.write(current_degree[servo3_pin]);
  myServo4.write(current_degree[servo4_pin]);

 
}





