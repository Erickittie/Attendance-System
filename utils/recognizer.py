import cv2
import pickle
import numpy as np

from config import (
    FACE_DETECT_MODEL,
    FACE_RECOGNITION_MODEL,
    EMBEDDINGS_PATH,
    FACE_SIMILARITY_THRESHOLD
)

# Load YuNet
detector = cv2.FaceDetectorYN.create(
    FACE_DETECT_MODEL,
    "",
    (320, 320),
    score_threshold=0.8,
    nms_threshold=0.3,
    top_k=5000
)

# Load SFace
recognizer = cv2.FaceRecognizerSF.create(
    FACE_RECOGNITION_MODEL,
    ""
)

# Load embeddings
with open(EMBEDDINGS_PATH, "rb") as f:
    known_embeddings = pickle.load(f)


def recognize(frame):

    h, w = frame.shape[:2]
    detector.setInputSize((w, h))

    _, faces = detector.detect(frame)

    if faces is None:
        return frame

    for face in faces:

        aligned = recognizer.alignCrop(frame, face)

        feature = recognizer.feature(aligned)

        best_match = "Unknown"
        best_score = 0

        for student_id, embedding_list in known_embeddings.items():

            for stored_feature in embedding_list:

                score = recognizer.match(
                    feature,
                    stored_feature,
                    cv2.FaceRecognizerSF_FR_COSINE
                )

                if score > best_score:
                    best_score = score
                    best_match = student_id

        x, y, w, h = face[:4].astype(int)

        if best_score >= FACE_SIMILARITY_THRESHOLD:

            color = (0, 255, 0)

            label = f"{best_match} ({best_score:.2f})"

        else:

            color = (0, 0, 255)

            label = "Unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        cv2.putText(
            frame,
            label,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    return frame