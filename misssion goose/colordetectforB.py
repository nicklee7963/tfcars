import cv2
import numpy as np
import serial  # 需確保已安裝 pyserial
color_message = " "
# 設定串行通訊（請根據實際端口和波特率進行修改）
ser = serial.Serial('COM18', 9600)  # 替換為你的端口
send_ser = serial.Serial('COM10', 9600, timeout=1)  # 發送到另一個 Arduino 的端口

# 定義藍色的 HSV 顏色範圍，並加上誤差
# blue_hue = 93
# blue_saturation = 248
# blue_value = 211
# blue_hue_range = 20
# blue_saturation_range = 50
# blue_value_range = 50

lower_blue = np.array([
    # max(blue_hue - blue_hue_range, 0), 
    # max(blue_saturation - blue_saturation_range, 0), 
    # max(blue_value - blue_value_range, 0)
    90,0,0
])
upper_blue = np.array([
    # min(blue_hue + blue_hue_range, 179), 
    # min(blue_saturation + blue_saturation_range, 255), 
    # min(blue_value + blue_value_range, 255)
    110,255,255
])

# 定義綠色的 HSV 顏色範圍
green_hue = 85
green_saturation = 244
green_value = 71
green_hue_range = 20
green_saturation_range = 50
green_value_range = 50

lower_green = np.array([
    max(green_hue - green_hue_range, 0), 
    max(green_saturation - green_saturation_range, 0), 
    max(green_value - green_value_range, 0)
])
upper_green = np.array([
    min(green_hue + green_hue_range, 179), 
    min(green_saturation + green_saturation_range, 255), 
    min(green_value + green_value_range, 255)
])

# 定義紅色的 HSV 顏色範圍
red_hue1 = 0
red_hue2 = 10
red_saturation = 187
red_value = 158
red_hue_range = 10
red_saturation_range = 50
red_value_range = 50

lower_red1 = np.array([
    # max(red_hue1 - red_hue_range, 0), 
    # max(red_saturation - red_saturation_range, 0), 
    # max(red_value - red_value_range, 0)
    0,0,0
])
upper_red1 = np.array([
    # min(red_hue1 + red_hue_range, 179), 
    # min(red_saturation + red_saturation_range, 255), 
    # min(red_value + red_value_range, 255)
    5,255,255
])

lower_red2 = np.array([
    # max(red_hue2 - red_hue_range, 0), 
    # max(red_saturation - red_saturation_range, 0), 
    # max(red_value - red_value_range, 0)
    175,0,0
])
upper_red2 = np.array([
    # min(red_hue2 + red_hue_range, 179), 
    # min(red_saturation + red_saturation_range, 255), 
    # min(red_value + red_value_range, 255)
    180,255,255
])

# 開始攝影機
cap = cv2.VideoCapture(0)

while True:
    # 讀取串行通訊
    if ser.in_waiting > 0:
        color_message = ser.readline().decode('utf-8').strip()  # 讀取顏色訊息

    ret, frame = cap.read()
    if not ret:
        break

    # 檢查收到的顏色訊息
    if color_message == "blue":
        # 藍色檢測
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
    elif color_message == "green":
        # 綠色檢測
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_green, upper_green)
    elif color_message == "red":
        # 紅色檢測
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)  # 合併紅色掩碼
    else:
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)  # 如果不是已知顏色則設為空掩碼

    # 計算掩碼的矩
    moments = cv2.moments(mask)

    if moments['m00'] > 0:  # 檢查是否有顏色物體
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])

        # 繪製物體的邊界框
        box_size = 30  # 調整框的大小
        cv2.rectangle(frame, (cx - box_size, cy - box_size), (cx + box_size, cy + box_size), (0, 255, 0), 2)

        # 檢查物體是否在畫面中心區域
        height, width, _ = frame.shape
        if (width // 2 - 50 < cx < width // 2 + 50) and (height // 2 - 50 < cy < height // 2 + 50):
            cv2.putText(frame, f"{color_message.capitalize()} in center!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            try:
                send_ser.write(b'1')  # 發送訊息 '1' 給另一個 Arduino
            except serial.SerialTimeoutException:
                print("Write timeout occurred")

    # 顯示影像
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源
cap.release()
ser.close()  # 關閉串行通訊
send_ser.close()  # 關閉發送到另一個 Arduino 的串行通訊
cv2.destroyAllWindows()
