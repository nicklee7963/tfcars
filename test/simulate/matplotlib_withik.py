import numpy as np
import matplotlib.pyplot as plt
from ikpy.chain import Chain
from ikpy.link import Link

# 定义机械臂链的结构
chain = Chain(name='robot_arm', links=[
    Link(
        name="link1",
        translation_vector=[0, 0, 0],
        orientation=[0, 0, 0, 1],
        joint_type="revolute"
    ),
    Link(
        name="link2",
        translation_vector=[10, 0, 0],
        orientation=[0, 0, 0, 1],
        joint_type="revolute"
    ),
    Link(
        name="link3",
        translation_vector=[8, 0, 0],
        orientation=[0, 0, 0, 1],
        joint_type="revolute"
    ),
])

# 定义目标位置
target_position = [15, 5, 0]

# 计算逆运动学
target_3d_position = np.array(target_position)
joint_angles = chain.inverse_kinematics(target_position=target_3d_position)

# 打印关节角度
print("Calculated joint angles (radians):", joint_angles)

# 绘制机械臂
fig, ax = plt.subplots()
ax.set_aspect('equal')

# 计算机械臂末端位置
end_effector_position = chain.forward_kinematics(joint_angles)[:3]

# 绘制机械臂
link_lengths = [0, 10, 8]  # 每段的长度

x = [0]
y = [0]

# 绘制每个连接段
current_position = np.array([0, 0])
for i, angle in enumerate(joint_angles):
    link_length = link_lengths[i]
    x_end = current_position[0] + link_length * np.cos(angle)
    y_end = current_position[1] + link_length * np.sin(angle)
    x.append(x_end)
    y.append(y_end)
    current_position = np.array([x_end, y_end])

# 绘制机械臂
ax.plot(x, y, 'bo-', label='Robot Arm')
ax.plot(target_position[0], target_position[1], 'r*', label='Target Position')

# 设置绘图范围和标签
ax.set_xlim(-1, 30)
ax.set_ylim(-1, 20)
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_title('二维机械臂示意图')
ax.legend()
ax.grid(True)

plt.show()
