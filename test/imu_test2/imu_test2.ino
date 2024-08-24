#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// IMU 对象
Adafruit_MPU6050 mpu;

// 角度计算相关变量
float angleZ = 0.0; // 角度（以度为单位）
float gyroZ_angle = 0.0; // 陀螺仪角度（以度为单位）
float gyroZ_bias = 0.0; // 陀螺仪偏置
unsigned long lastTime;
float dt;

// 互补滤波器参数
float alpha = 0.98; // 互补滤波器的平滑因子

void setup() {
    // 初始化串口
    Serial.begin(115200);
    Serial.println("MPU6050 Angle Test");

    // 初始化 IMU
    if (!mpu.begin()) {
        Serial.println("Failed to find MPU6050 chip");
        while (1);
    }

    // 设置 IMU 量程
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

    // 计算陀螺仪偏置
    float gyroZ_sum = 0.0;
    const int numSamples = 100;
    for (int i = 0; i < numSamples; i++) {
        sensors_event_t a, g, temp;
        mpu.getEvent(&a, &g, &temp);
        gyroZ_sum += g.gyro.z;
        delay(10); // 延时以便采集
    }
    gyroZ_bias = gyroZ_sum / numSamples;
    
    // 初始化时间
    lastTime = millis();
}

void loop() {
    // 读取IMU数据
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    unsigned long now = millis();
    dt = (now - lastTime) / 1000.0; // 计算时间差
    lastTime = now;

    // 获取陀螺仪数据，并应用偏置补偿
    float gyroZ = g.gyro.z - gyroZ_bias;

    // 计算陀螺仪角度（基于陀螺仪积分）
    gyroZ_angle += gyroZ * dt;

    // 直接使用陀螺仪角度作为最终的角度
    angleZ = gyroZ_angle;

    // 打印角度数据
    Serial.print("Gyro Z Angle: "); Serial.print(gyroZ_angle); Serial.print(" degrees ");
    Serial.print("Filtered Angle Z: "); Serial.print(angleZ); Serial.println(" degrees");

    delay(100); // 延时 100 毫秒
}
