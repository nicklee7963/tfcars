import cv2
import numpy as np
import serial

# 設置 Arduino 的串口連接（根據實際情況設置 COM 端口和波特率）
arduino = serial.Serial('COM17', 9600)  # 請根據你的 Arduino 連接情況調整 COM 端口

# 定義黃色的顏色範圍
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# 設置黃色像素數量的閾值
yellow_threshold = 500  # 根據需要調整這個閾值

# 啟動攝像頭
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 轉換顏色空間
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 創建遮罩
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 去噪處理
    mask = cv2.medianBlur(mask, 5)

    # 檢測特定顏色
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # 計算黃色像素數量
    yellow_pixel_count = np.sum(mask == 255)

    # 顯示結果
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', result)

    # 檢查是否檢測到足夠多的黃色像素
    if yellow_pixel_count > yellow_threshold:
        # 發送信號到 Arduino 控制雷射模組
        arduino.write(b'H')  # 發送 'H' 來打開雷射
    else:
        # 關閉雷射模組
        arduino.write(b'L')  # 發送 'L' 來關閉雷射

    # 按下 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源
cap.release()
cv2.destroyAllWindows()
arduino.close()
