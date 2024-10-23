import cv2
import numpy as np

# 用于输入三种颜色的 HSV 上下限
# 可以手动输入红色、绿色、蓝色的上下限 (H, S, V)
red_lower = np.array([0, 50, 50])   # 红色 HSV 下限
red_upper = np.array([10, 255, 255])  # 红色 HSV 上限

green_lower = np.array([35, 50, 50])  # 绿色 HSV 下限
green_upper = np.array([85, 255, 255])  # 绿色 HSV 上限

blue_lower = np.array([100, 50, 50])  # 蓝色 HSV 下限
blue_upper = np.array([140, 255, 255])  # 蓝色 HSV 上限

def detect_color(hsv_frame):
    # 检测红色区域
    red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)
    red_output = cv2.bitwise_and(frame, frame, mask=red_mask)

    # 检测绿色区域
    green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)
    green_output = cv2.bitwise_and(frame, frame, mask=green_mask)

    # 检测蓝色区域
    blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)
    blue_output = cv2.bitwise_and(frame, frame, mask=blue_mask)

    return red_output, green_output, blue_output

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("无法打开摄像头")
        break
    
    # 转换为 HSV 图像
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 检测颜色
    red_detected, green_detected, blue_detected = detect_color(hsv_frame)

    # 显示原始帧和检测到的颜色
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Red Detected', red_detected)
    cv2.imshow('Green Detected', green_detected)
    cv2.imshow('Blue Detected', blue_detected)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
