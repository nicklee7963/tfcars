import cv2
import numpy as np
import serial  # 確保已安裝 pyserial
import time

color_message = " "
# 設定串行通訊（根據實際端口和波特率修改）
ser = serial.Serial('/dev/arduino_scale', 9600)  # weight_lcd
send_ser = serial.Serial('/dev/arduino_arm', 9600, timeout=1)  # arm
wheels = serial.Serial('/dev/arduino_wheel', 9600, timeout=1)  # wheels
wheels.flush()
control = serial.Serial('/dev/arduino_led', 9600, timeout=1)  # control LED/Laser
control.flush()

# 定義藍色、綠色、紅色的 HSV 顏色範圍（與原本相同，省略重複部分）

blue_hue = 93
blue_saturation = 248
blue_value = 211
blue_hue_range = 20
blue_saturation_range = 50
blue_value_range = 50

lower_blue = np.array([
    #max(blue_hue - blue_hue_range, 0),
    #max(blue_saturation - blue_saturation_range, 0),
    #max(blue_value - blue_value_range, 0)
    94,0,0
])
upper_blue = np.array([
    #min(blue_hue + blue_hue_range, 179),
    #min(blue_saturation + blue_saturation_range, 255),
    #min(blue_value + blue_value_range, 255)
    100,255,255
])

# 定義綠色的 HSV 顏色範圍
green_hue = 85
green_saturation = 244
green_value = 71
green_hue_range = 20
green_saturation_range = 50
green_value_range = 50

lower_green = np.array([
    # max(green_hue - green_hue_range, 0),
    # max(green_saturation - green_saturation_range, 0),
    # max(green_value - green_value_range, 0)
    68,0,0
])
upper_green = np.array([
    # min(green_hue + green_hue_range, 179),
    # min(green_saturation + green_saturation_range, 255),
    # min(green_value + green_value_range, 255)
    85,255,255
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
    #max(red_hue1 - red_hue_range, 0),
    #max(red_saturation - red_saturation_range, 0),
    #max(red_value - red_value_range, 0)
    0,0,0
])
upper_red1 = np.array([
    #min(red_hue1 + red_hue_range, 179),
    #min(red_saturation + red_saturation_range, 255),
    #min(red_value + red_value_range, 255)
    3,255,255
])

lower_red2 = np.array([
    #max(red_hue2 - red_hue_range, 0),
    #max(red_saturation - red_saturation_range, 0),
    #max(red_value - red_value_range, 0)
    177,0,0
])
upper_red2 = np.array([
    #min(red_hue2 + red_hue_range, 179),
    #min(red_saturation + red_saturation_range, 255),
    #min(red_value + red_value_range, 255)
    180,255,255
])

def control_wheels(command):
    """控制前後輪的運動"""
    wheels.write(command.encode('utf-8'))

def control_parts(command):
    """控制LED、雷射等元件"""
    control.write(command.encode('utf-8'))

def process_a_task(frame):
    """
    處理 A 關卡，根據接收到的顏色訊息進行動作。
    """
    global color_message

    # 檢查串行通訊中是否有資料
    if ser.in_waiting > 0:
        color_message = ser.readline().decode('utf-8').strip().lower()  # 讀取顏色訊息

    # 如果 frame 為 None，則返回錯誤
    if frame is None or frame.size == 0:
        print("Error: Invalid frame received.")
        return

    # 根據 color_message 進行顏色檢測
    if color_message == "blue":
        print("Find BLUE!")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
    elif color_message == "green":
        print("Find GREEN!")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_green, upper_green)
    elif color_message == "red":
        print("Find RED!")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)  # 如果顏色無效，空掩碼

    # 計算掩碼的有效像素數量
    color_area = cv2.countNonZero(mask)

    # 設置一個顏色區域的最小閾值（例如5000像素）
    area_threshold = 5000

    if color_area > area_threshold:  # 只有當區域大於閾值時，才進行下一步
        # 計算掩碼的矩
        moments = cv2.moments(mask)

        # 如果檢測到顏色物體
        if moments['m00'] > 0:
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])

            # 檢查物體是否位於畫面中央
            height, width, _ = frame.shape
            if (width // 2 - 50 < cx < width // 2 + 50) and (height // 2 - 50 < cy < height // 2 + 50):
                cv2.putText(frame, f"{color_message.capitalize()} in center!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                try:
                    control_wheels('A')  # 停止車輪
                    control_parts('Y')  # 亮起黃色LED燈
                    send_ser.write(b'P')  # 控制夾取動作
                    time.sleep(3)  # 假設手臂需要一秒執行

                    # 發送完成訊息給 main.py
                    print("A 關卡完成，返回主程序")
                    return "a_done"  # 返回完成訊息

                except serial.SerialTimeoutException:
                    print("串行通訊超時")

    # 若需要，這裡可以顯示或傳回處理後的影像
    # cv2.imshow('Processed Frame', frame)

# Example usage:
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image from camera.")
            break
        process_a_task(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
