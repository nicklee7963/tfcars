#include <MPU6050_light.h>
#include <Wire.h>

// 创建 MPU6050 对象
MPU6050 mpu(Wire);

void setup() {
  Serial.begin(9600);
  Wire.begin();

  byte status = mpu.begin();
  if (status != 0) {
    Serial.println("MPU6050 初始化失败");
    while (1);
  }

  Serial.println("MPU6050 初始化成功");
  mpu.calcOffsets(true, true); // 校准陀螺仪和加速度计

}

void loop() {
  mpu.update();

  Serial.print("加速度计 X轴: ");
  Serial.print(mpu.getAccX());
  Serial.print("\tY轴: ");
  Serial.print(mpu.getAccY());
  Serial.print("\tZ轴: ");
  Serial.println(mpu.getAccZ());

  Serial.print("陀螺仪 X轴: ");
  Serial.print(mpu.getGyroX());
  Serial.print("\tY轴: ");
  Serial.print(mpu.getGyroY());
  Serial.print("\tZ轴: ");
  Serial.println(mpu.getGyroZ());

  delay(1000);
}