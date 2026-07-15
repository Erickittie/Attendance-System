import cv2
from config import FACE_DETECT_MODEL

detector = cv2.FaceDetectorYN.create(
    FACE_DETECT_MODEL,
    "",
    (320, 320),
    score_threshold=0.8,
    nms_threshold=0.3,
    top_k=5000
)

def detect_faces(frame):
    h, w = frame.shape[:2]
    detector.setInputSize((w, h))

    _, faces = detector.detect(frame)

    return faces