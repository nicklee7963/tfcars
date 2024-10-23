import cv2
import numpy as np
import serial
import time

color_message = " "
# 設定串行通訊（根據實際端口和波特率修改）
ser = serial.Serial('/dev/arduino_scale', 9600)
send_ser = serial.Serial('/dev/arduino_arm', 9600, timeout=1)
wheels = serial.Serial('/dev/arduino_wheel', 9600, timeout=1)
control = serial.Serial('/dev/arduino_led', 9600, timeout=1)

# 定義顏色的 HSV 範圍
lower_blue = np.array([94, 0, 0])
upper_blue = np.array([100, 255, 255])
lower_green = np.array([68, 0, 0])
upper_green = np.array([85, 255, 175])
lower_red1 = np.array([0, 0, 0])
upper_red1 = np.array([3, 255, 255])
lower_red2 = np.array([177, 0, 0])
upper_red2 = np.array([180, 255, 255])

def control_wheels(command):
    wheels.write(command.encode('utf-8'))

def control_parts(command):
    control.write(command.encode('utf-8'))

def process_a_task(frame):
    global color_message

    if ser.in_waiting > 0:
        color_message = ser.readline().decode('utf-8').strip().lower()

    if frame is None or frame.size == 0:
        print("Error: Invalid frame.")
        return

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = None

    if color_message == "blue":
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
    elif color_message == "green":
        mask = cv2.inRange(hsv, lower_green, upper_green)
    elif color_message == "red":
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

    if mask is None:
        return

    color_area = cv2.countNonZero(mask)
    area_threshold = 50000

    if color_area > area_threshold:
        moments = cv2.moments(mask)
        if moments['m00'] > 0:
            cx = int(moments['m10'] / moments['m00'])
            width = frame.shape[1]

            # 只判斷 x 座標是否在中間
            if width // 2 - 50 < cx < width // 2 + 50:
                control_wheels('A')  # 停止車輪
                control_parts('Y')  # 亮起LED
                send_ser.write(b'P')  # 控制夾取
                time.sleep(3)
                print("A 關卡完成")
                return "a_done"

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break
        process_a_task(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
