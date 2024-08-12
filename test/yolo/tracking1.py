from ultralytics import YOLO 
import cv2

# 載入訓練好的 YOLO 模型
model = YOLO('runs/detect/train7/weights/best.pt')

# 打開攝影機
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

idset = set()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # 使用模型進行物件追蹤
    try:
        results = model(frame)  # 改成使用推理方法來替代 track 方法
        print("Model inference success")
    except Exception as e:
        print(f"Model inference error: {e}")
        break

    # 處理推理結果
    for result in results:
        for box in result.boxes:
            track_id = box.id

            if track_id is None:
                print("Track ID is None, skipping this box")
                continue
            
            if track_id not in idset:
                # 確保 xyxy 變成四個座標的向量
                x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                confidence = box.conf.item()
                class_id = int(box.cls.item())

                # 繪製矩形框和標籤
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Class {class_id}: {confidence:.2f} ID:{track_id}", 
                            (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                idset.add(track_id)
    
    # 顯示結果
    cv2.imshow("result", frame)

    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝影機並關閉所有 OpenCV 視窗
cap.release()
cv2.destroyAllWindows()
