import cv2
from PIL import Image
import time
import numpy as np

bgr_color = [0, 255, 255]


def pick_color(event, x, y, flags, param):
    global bgr_color
    frame = param  # 获取传递的 frame 参数
    if event == cv2.EVENT_LBUTTONDOWN:  # 如果检测到鼠标左键按下事件
        print("")
        # 获取点击位置的像素值 (BGR)
        bgr_color = frame[y, x]
        b, g, r = bgr_color
        print(f"Selected BGR color: B={b}, G={g}, R={r}")

        # 转换为HSV颜色
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
        h, s, v = hsv_color[0][0]
        print(f"Selected HSV color: H={h}, S={s}, V={v}")

        # 显示选中的颜色块
        color_patch = np.zeros((100, 100, 3), np.uint8)
        color_patch[:] = bgr_color
        cv2.imshow('Selected Color', color_patch)

def get_limits(color, tolerance=5):
    # 将 BGR 转换为 HSV
    hsv_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_BGR2HSV)
    h, s, v = hsv_color[0][0]

    # 设置 HSV 颜色范围
    lower_limit = np.array([max(0, h - tolerance), max(0, s - tolerance), max(0, v - tolerance)])
    upper_limit = np.array([min(180, h + tolerance), min(255, s + tolerance), min(255, v + tolerance)])

    return lower_limit, upper_limit

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (0, 0, 255)
thickness = 2
position = (10, 50)

delay = 0.1
cap = cv2.VideoCapture(0)
cv2.namedWindow('frame')

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("can't open camera")
        break
    
    # 传递 frame 给回调函数
    cv2.setMouseCallback('frame', pick_color, frame)
    
    hsvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerLimit, upperLimit = get_limits(color=bgr_color, tolerance=10)
    mask = cv2.inRange(hsvimage, lowerLimit, upperLimit)
    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()
    time.sleep(delay)
    
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.putText(frame, "color detected", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        detect_center = (x1 + x2) / 2
        height, width = frame.shape[:2]
        frame_center = width / 2
        
        if frame_center - 20 < detect_center < frame_center + 20:
            cv2.putText(frame, "Don't move", position, font, font_scale, color, thickness)
        elif detect_center < frame_center - 20:
            cv2.putText(frame, "Move right", position, font, font_scale, color, thickness)
        elif detect_center > frame_center + 20:
            cv2.putText(frame, "Move left", position, font, font_scale, color, thickness)
    else:
        cv2.putText(frame, "no color detected", position, font, font_scale, color, thickness)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
