import cv2
import os
import pickle
import numpy as np

from config import (
    FACE_DETECT_MODEL,
    FACE_RECOGNITION_MODEL,
    DATASET_PATH,
    EMBEDDINGS_PATH
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


def generate_embeddings():

    embeddings = {}

    for student_id in os.listdir(DATASET_PATH):

        student_folder = os.path.join(DATASET_PATH, student_id)

        if not os.path.isdir(student_folder):
            continue

        embeddings[student_id] = []

        for image_name in os.listdir(student_folder):

            image_path = os.path.join(student_folder, image_name)

            image = cv2.imread(image_path)

            if image is None:
                continue

            h, w = image.shape[:2]

            detector.setInputSize((w, h))

            _, faces = detector.detect(image)

            if faces is None:
                continue

            face = faces[0]

            aligned = recognizer.alignCrop(image, face)

            feature = recognizer.feature(aligned)

            embeddings[student_id].append(feature)

    with open(EMBEDDINGS_PATH, "wb") as file:
        pickle.dump(embeddings, file)

    print("Embeddings saved successfully!")