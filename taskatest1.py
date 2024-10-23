import cv2
import numpy as np
import time

# 顏色範圍設置
lower_blue = np.array([94, 0, 0])
upper_blue = np.array([100, 255, 255])

lower_green = np.array([68, 0, 0])
upper_green = np.array([85, 255, 140])

lower_red1 = np.array([0, 0, 0])
upper_red1 = np.array([3, 255, 255])

lower_red2 = np.array([177, 0, 0])
upper_red2 = np.array([180, 255, 255])

def process_a_task(frame, color_message):
    """
    處理 A 關卡，根據顏色進行動作，並顯示 OK 或 NO，還會判斷 X 座標是否在中心。
    """
    if frame is None or frame.size == 0:
        print("Error: Invalid frame received.")
        return

    if color_message == "blue":
        print("Detecting BLUE!")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
    elif color_message == "green":
        print("Detecting GREEN!")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_green, upper_green)
    elif color_message == "red":
        print("Detecting RED!")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)  # 如果顏色無效，空掩碼

    # 計算掩碼的有效像素數量
    color_area = cv2.countNonZero(mask)

    # 設置一個顏色區域的最小閾值（例如 10000 像素）
    area_threshold = 10000

    # 只在區域超過閾值時檢查 X 座標是否在中心
    if color_area > area_threshold:
        moments = cv2.moments(mask)
        if moments['m00'] > 0:  # 防止除以零
            cx = int(moments['m10'] / moments['m00'])  # 計算質心的 x 座標
            width = frame.shape[1]

            # 判斷質心是否在畫面中間
            if width // 2 - 50 < cx < width // 2 + 50:
                cv2.putText(frame, "OK", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                print(f"{color_message.capitalize()} detected, area is sufficient, and x is centered!")
            else:
                cv2.putText(frame, "X NOT CENTERED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
                print(f"{color_message.capitalize()} detected, but x is NOT centered.")
        else:
            print(f"{color_message.capitalize()} moments invalid.")
    else:
        cv2.putText(frame, "NO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        print(f"{color_message.capitalize()} area not sufficient.")

    # 顯示畫面中的變更
    cv2.imshow('Processed Frame', frame)

# Example usage:
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    color_message = "red"  # 假設我們要檢測顏色，可以更改此值以測試不同顏色
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image from camera.")
            break

        # 處理影像並檢測顏色區域
        process_a_task(frame, color_message)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
