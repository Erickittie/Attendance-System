import os

# ===========================
# DATABASE CONFIGURATION
# ===========================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "erick123",
    "database": "attendance_db"
}

# ===========================
# CAMERA
# ===========================

CAMERA_SOURCE = 0

# ===========================
# MODELS
# ===========================

FACE_DETECT_MODEL = "models/yunet.onnx.onnx"
FACE_RECOGNITION_MODEL = "models/face_recognition_sface_2021dec.onnx"

# ===========================
# FILES
# ===========================

DATASET_PATH = "dataset"
EMBEDDINGS_PATH = "embeddings/embeddings.pkl"

CSV_FOLDER = "attendance_csv"

# ===========================
# FACE THRESHOLD
# ===========================

FACE_SIMILARITY_THRESHOLD = 0.55