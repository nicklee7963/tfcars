from ultralytics import YOLO
model = YOLO("C:/Users/acer0926/runs/detect/train6/weights/best.pt")
model.predict(source = "D:/opencv_python/tfcars/object_detect/1.jpg")