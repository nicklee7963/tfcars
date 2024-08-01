from ultralytics import YOLO

# 創建 YOLOv8 模型實例
model = YOLO('yolov8n.yaml')  # 選擇適當的 YOLOv8 模型配置

# 開始訓練

model.train(
    data=r'D:/opencv_python/tfcars/object_detect/data.yaml',
    epochs=100,
    imgsz=640,
    batch=8,
    project='runs/train',
    name='yolov8_experiment',
    
)
