import numpy as np
import matplotlib.pyplot as plt

# 设定手臂段长度
L1 = 100
L2 = 50

def calculate_joint_angles(x, y):
    # 计算目标点到原点的距离
    D = np.sqrt(x**2 + y**2)
    
    # 检查目标点是否在手臂的工作范围内
    if D > L1 + L2:
        raise ValueError("目标点超出手臂的工作范围")

    # 计算第一段手臂的角度
    phi = np.arctan2(y, x)
    cos_theta = (D**2 + L1**2 - L2**2) / (2 * D * L1)
    theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    cos_angle = (D**2 + L2**2 - L1**2) / (2 * D * L2)
    angle = np.arccos(cos_angle)
    theta1 = phi + theta
    theta2 = phi - angle 
    
    # 确保角度在 0 到 2π 之间
    phi_deg = np.degrees(phi)
    theta_deg = np.degrees(theta)
    angle_deg = np.degrees(angle)
    theta1_deg = np.degrees(theta1)
    theta2_deg = np.degrees(theta2)
    print(f"phi = {phi_deg}\ntheta = {theta_deg}\nangle = {angle_deg}")
    return theta1_deg, theta2_deg

def plot_arm(theta1, theta2, x_target, y_target):
    # 将角度从度转换回弧度
    theta1_rad = np.radians(theta1)
    theta2_rad = np.radians(theta2)
    
    # 计算关节位置
    x0, y0 = 0, 0
    x1 = L1 * np.cos(theta1_rad)
    y1 = L1 * np.sin(theta1_rad)
    x2 = x1 + L2 * np.cos(theta2_rad)
    y2 = y1 + L2 * np.sin(theta2_rad)

    # 绘制手臂
    plt.figure()
    plt.plot([x0, x1], [y0, y1], 'ro-', lw=2, label='Arm Segment 1')
    plt.plot([x1, x2], [y1, y2], 'bo-', lw=2, label='Arm Segment 2')
    plt.plot(x2, y2, 'go', markersize=10, label='End-Effector')  # 手臂末端
    plt.plot(x_target, y_target, 'mo', markersize=10, label='Target')  # 目标点
    plt.xlim(-150, 150)
    plt.ylim(-150, 150)
    
    # 设置坐标轴
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title('2D Arm Simulation')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

# 目标位置
x_target = 130
y_target = 20

# 计算关节角度
theta1, theta2 = calculate_joint_angles(x_target, y_target)

# 打印角度（度）
print(f"Theta1 (degrees): {theta1:.2f}")
print(f"Theta2 (degrees): {theta2:.2f}")

# 绘制手臂并显示目标点
plot_arm(theta1, theta2, x_target, y_target)
