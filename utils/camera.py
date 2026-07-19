import cv2


camera = cv2.VideoCapture(0)


current_frame = None



def get_frame():

    global current_frame


    success, frame = camera.read()


    if success:

        current_frame = frame


    return current_frame



def generate_frames():

    while True:


        frame = get_frame()


        if frame is None:
            continue



        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )


        frame = buffer.tobytes()



        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame +
            b"\r\n"
        )