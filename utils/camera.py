import cv2

def open_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Cannot read frame.")
            break

        cv2.imshow("Attendance Camera", frame)

        key = cv2.waitKey(1)

        if key == 27:   # ESC
            break

    cap.release()
    cv2.destroyAllWindows()