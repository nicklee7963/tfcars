from ultralytics import YOLO 
import cv2


model = YOLO("<your model>")
cap = cv2.VideoCapture(0)



idset = set()
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model.track(frame)



    for result in results:
        for box in result.boxes:
            track_id = box.id
            if track_id not in idset:
                x1, y1, x2, y2 = map(int, box,xyxy)
                confidence = box.conf
                class_id = box.cls

                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(frame, f"{class_id}: {confidence:.2f} ID:{track.id}"(x1,y1-10), cv2,FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)

                idset.add(track_id)
            cv2.imshow("result", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
