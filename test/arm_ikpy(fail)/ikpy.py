import serial
import time
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLin
import numpy as np

# 設置串口連接
ser = serial.Serial('COM3', 9600)  # 根據你的串口配置進行修改

# 定義機械臂的鏈結結構
chain = Chain(name='robot_arm', links=[
    OriginLink(),
    URDFLink(
        name="link1",
        translation_vector=[0, 0, 1],
        orientation=[0, 0, 0, 1],
        bounds=(-np.pi, np.pi)
    ),
    URDFLink(
        name="link2",
        translation_vector=[1, 0, 0],
        orientation=[0, 0, 0, 1],
        bounds=(-np.pi, np.pi)
    ),
    URDFLink(
        name="link3",
        translation_vector=[0, 1, 0],
        orientation=[0, 0, 0, 1],
        bounds=(-np.pi, np.pi)
    ),
])

def move_servos(angles):
    # 將角度轉換為伺服信號範圍（假設是0到180度）
    servo_angles = [int(angle * 180 / np.pi) for angle in angles]

    # 生成指令並發送到伺服馬達
    for i, angle in enumerate(servo_angles):
        command = f"{i+1}:{angle}\n"
        ser.write(command.encode())
        time.sleep(0.1)  # 確保每個指令都被處理

# 設定目標位置
target_position = [1, 1, 1]

# 計算逆向運動學解
angles = chain.inverse_kinematics(target_position)

# 印出結果
print("Inverse Kinematics Angles:", angles)

# 控制伺服馬達
move_servos(angles)

# 關閉串口連接
ser.close()
