from ultralytics import YOLO
import cv2

def process_detections(results, detected_objects, frame, model_type):
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf.item()
            class_id = int(box.cls.item())
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            
            # Create a unique key for each detected object
            unique_key = (center_x, center_y, class_id, model_type)
            if unique_key in detected_objects:
                continue  # Skip already detected objects
            
            detected_objects.add(unique_key)
            
            # Determine color based on position
            color = (0, 255, 0) if is_center(center_x, center_y, frame) else (0, 0, 255)
            
            # Draw bounding box and label
            label = f"{model_type} {class_id}: {confidence:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 5)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 5)
            cv2.circle(frame, (center_x, center_y), 5, color, -1)
            
            # Only trigger actions if the object is in the center of the frame
            if is_center(center_x, center_y, frame):
                if model_type == "chick" and class_id == 0:
                    # Trigger pink chick removal 
                    pass
                elif model_type == "wild_bird" and class_id == 0:
                    # Trigger rooster action
                    pass
                elif model_type == "wild_bird" and class_id == 1:
                    # Trigger mynah bird action
                    pass

def is_center(center_x, center_y, frame):
    frame_center_x = frame.shape[1] // 2
    frame_center_y = frame.shape[0] // 2
    # Define a threshold for what is considered "center"
    threshold = 50
    return abs(center_x - frame_center_x) < threshold and abs(center_y - frame_center_y) < threshold

# Load your models
chick_model = YOLO('runs/detect/train_chick/weights/best.pt')
wild_bird_model = YOLO('runs/detect/train_bird/weights/best.pt')

# Open the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Set to store detected objects
detected_objects = set()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Detect chicks first
    chick_results = chick_model(frame)
    process_detections(chick_results, detected_objects, frame, "chick")

    # Detect wild birds next
    wild_bird_results = wild_bird_model(frame)
    process_detections(wild_bird_results, detected_objects, frame, "wild_bird")
    
    # Show the frame
    cv2.imshow("Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
