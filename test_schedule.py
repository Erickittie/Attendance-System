import cv2

from utils.camera import open_camera
from utils.ocr import read_text

camera = open_camera()

while True:

    ret, frame = camera.read()

    texts = read_text(frame)

    for text in texts:

        print(text)

    cv2.imshow("OCR", frame)

    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()