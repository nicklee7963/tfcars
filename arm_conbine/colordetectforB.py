import cv2
import numpy as np
import serial  # 需確保已安裝 pyserial
color_message = " "
# 設定串行通訊（請根據實際端口和波特率進行修改）
ser = serial.Serial('COM18', 9600)  # 替換為你的端口
send_ser = serial.Serial('COM10', 9600)  # 替換為發送到另一個 Arduino 的端口

# 定義藍色的 HSV 顏色範圍，並加上誤差
hue = 93
saturation = 248
value = 211
hue_range = 20
saturation_range = 50
value_range = 50

lower_blue = np.array([max(hue - hue_range, 0), max(saturation - saturation_range, 0), max(value - value_range, 0)])
upper_blue = np.array([min(hue + hue_range, 179), min(saturation + saturation_range, 255), min(value + value_range, 255)])

# 開始攝影機
cap = cv2.VideoCapture(0)

while True:
    # 讀取串行通訊
    if ser.in_waiting > 0:
        color_message = ser.readline().decode('utf-8').strip()  # 讀取顏色訊息

    ret, frame = cap.read()
    if not ret:
        break

    # 只在收到 "blue" 時進行藍色檢測
    if color_message == "blue":
        # 將影像轉換為 HSV 顏色空間
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 創建藍色的掩碼
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # 計算掩碼的矩
        moments = cv2.moments(mask)

        if moments['m00'] > 0:  # 檢查是否有藍色物體
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])

            # 繪製藍色物體的邊界框
            box_size = 30  # 調整框的大小
            cv2.rectangle(frame, (cx - box_size, cy - box_size), (cx + box_size, cy + box_size), (0, 255, 0), 2)

            # 檢查藍色物體是否在畫面中心區域
            height, width, _ = frame.shape
            if (width // 2 - 50 < cx < width // 2 + 50) and (height // 2 - 50 < cy < height // 2 + 50):
                cv2.putText(frame, "Blue in center!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                send_ser.write(b'1')  # 發送訊息 '1' 給另一個 Arduino
            else:
                send_ser.write(b'0')

    # 顯示影像
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源
cap.release()
ser.close()  # 關閉串行通訊
send_ser.close()  # 關閉發送到另一個 Arduino 的串行通訊
cv2.destroyAllWindows()
