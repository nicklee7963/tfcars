import matplotlib.pyplot as plt
import numpy as np

# 定义机械臂各段的长度
length1 = 10
length2 = 8
length3 = 6

# 定义目标位置 (x, y)
x_target = 10
y_target = 5

# 计算角度（以弧度为单位）
theta1 = np.arctan2(y_target, x_target)
# 为简化起见，这里假设机械臂在目标位置的方向上完全伸展
# 实际应用中应使用逆运动学来计算角度

# 计算各段的末端位置
x1 = length1 * np.cos(theta1)
y1 = length1 * np.sin(theta1)

x2 = x1 + length2 * np.cos(theta1)
y2 = y1 + length2 * np.sin(theta1)

x3 = x2 + length3 * np.cos(theta1)
y3 = y2 + length3 * np.sin(theta1)

# 绘制机械臂
plt.figure()
plt.plot([0, x1], [0, y1], 'ro-', label='第一段')
plt.plot([x1, x2], [y1, y2], 'go-', label='第二段')
plt.plot([x2, x3], [y2, y3], 'bo-', label='第三段')
plt.plot(x_target, y_target, 'k*', label='目标位置')

# 设置绘图范围和标签
plt.xlim(-1, 20)
plt.ylim(-1, 15)
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.title('二维机械臂示意图')
plt.legend()
plt.grid(True)

plt.show()
