from ultralytics import YOLO

# 載入預訓練的 YOLOv8 細分模型
model = YOLO('yolov8n-seg.pt')

# 使用預訓練的 YOLOv8 模型進行推理
results = model.predict(
    source='D:/opencv_python/tfcars/object_detect/bus.jpg',
    conf=0.5  # 設定置信度閾值為 0.5
)

# 顯示檢測結果
results.plot()
