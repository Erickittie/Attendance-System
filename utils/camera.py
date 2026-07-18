import cv2


def open_camera():

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        raise Exception("Cannot open camera.")

    return camera