import cv2
from ultralytics import YOLO

model = YOLO("./runs/detect/train4/weights/best.pt")

# img = cv2.imread("a.jpg")
# img = cv2.flip(img, 1)      
# results = model.predict(source=img, save=True)  # save plotted images
# for r in results:
#     print(r.boxes.data)
# exit(0)

model = YOLO("./runs/detect/train4/weights/best.pt")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    frame = cv2.flip(frame, 1)
    results = model.predict(source=frame, conf=0.8, verbose=False)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    for r in results:
        for box in r.boxes.data:
            # Blue -> box[-1]==1.0 , RED -> box[-1]==0.0
            print(box[-1]==1.0)
            exit(0)
            # Extract the bounding box coordinates and convert them to integers
            x_min, y_min, x_max, y_max = map(int, box[:4])
            
            # Draw a rectangle on the frame using the bounding box coordinates
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            x_center = (x_min + x_max) / 2
            y_center = (y_min + y_max) / 2
    cv2.imshow('frame', frame)