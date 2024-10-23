import cv2
import numpy as np
import serial  # 確保已安裝 pyserial
import time

sleep = 0

color_message = " "
# 設定串行通訊（根據實際端口和波特率修改）
ser = serial.Serial('/dev/arduino_scale', 9600)  # weight_lcd
send_ser = serial.Serial('/dev/arduino_arm', 9600, timeout=1)  # arm
wheels = serial.Serial('/dev/arduino_wheel', 9600, timeout=1)  # wheels
wheels.flush()
control = serial.Serial('/dev/arduino_led', 9600, timeout=1)  # control LED/Laser
control.flush()

# 定義藍色的 HSV 顏色範圍
lower_blue = np.array([94, 0, 0])
upper_blue = np.array([100, 255, 255])

# 定義綠色的 HSV 顏色範圍
lower_green = np.array([68, 0, 0])
upper_green = np.array([85, 255, 175])

# 定義紅色的 HSV 顏色範圍
lower_red1 = np.array([0, 0, 0])
upper_red1 = np.array([3, 255, 255])
lower_red2 = np.array([177, 0, 0])
upper_red2 = np.array([180, 255, 255])

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
    global sleep  # 使用全局變數

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
        if sleep == 0:
            sleep = 1
            time.sleep(20)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
    elif color_message == "green":
        print("Find GREEN!")
        if sleep == 0:
            sleep = 1
            time.sleep(20)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_green, upper_green)
    elif color_message == "red":
        print("Find RED!")
        if sleep == 0:
            sleep = 1
            time.sleep(20)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)  # 如果顏色無效，空掩碼

    # 計算掩碼的有效像素數量
    color_area = cv2.countNonZero(mask)

    # 設置一個顏色區域的最小閾值（例如5000像素）
    area_threshold = 50000

    if color_area > area_threshold:  # 只有當區域大於閾值時，才進行下一步
        moments = cv2.moments(mask)
        if moments['m00'] > 0:
            cx = int(moments['m10'] / moments['m00'])

            height, width, _ = frame.shape
            if (width // 2 - 50 < cx < width // 2 + 50):  # 只檢查 cx
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
