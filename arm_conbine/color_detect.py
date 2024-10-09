import cv2
import numpy as np
import serial
import time

scale = serial.Serial('COM18', 9600)
time.sleep(2)

# 定義顏色範圍
def color_detection(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定義紅色範圍
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    # 調整暗綠色範圍
    lower_dark_green = np.array([30, 50, 50])  # 調整下限
    upper_dark_green = np.array([70, 255, 255])  # 調整上限
    
    # 定義藍色範圍
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([140, 255, 255])

    # 創建顏色掩碼
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    mask_dark_green = cv2.inRange(hsv, lower_dark_green, upper_dark_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    return mask_red, mask_dark_green, mask_blue, frame

# 開始攝影機
cap = cv2.VideoCapture(0)

while True:
    if scale.in_waiting > 0:
        data = scale.readline().decode('utf-8').strip()  # 讀取數據
    ret, frame = cap.read()
    if not ret:
        break

    mask_red, mask_dark_green, mask_blue, original_frame = color_detection(frame)

    # 找到輪廓
    for color_mask, color_name in zip([mask_red, mask_dark_green, mask_blue], ['Red', 'Dark Green', 'Blue']):
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # 可以根據需要調整面積閾值
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(original_frame, (x, y), (x + w, y + h), (0, 255, 0) if color_name == 'Dark Green' else (255, 0, 0) if color_name == 'Blue' else (0, 0, 255), 2)
                cv2.putText(original_frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # 顯示結果
    cv2.imshow('Detected Colors', original_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源
cap.release()
cv2.destroyAllWindows()
