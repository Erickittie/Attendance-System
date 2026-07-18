import cv2

from utils.ocr import detect_id_number
from utils.student import get_student
from utils.schedule import get_current_schedule
from utils.attendance import mark_attendance

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Cannot open camera.")
    exit()

last_id = ""
student = None
status = ""

while True:

    ret, frame = camera.read()

    if not ret:
        break

    # Detect ID Number
    id_number = detect_id_number(frame)

    if id_number and id_number != last_id:

        # Save last scanned ID
        last_id = id_number

        # Find student
        student = get_student(id_number)

        if student:

            schedule = get_current_schedule(
                student["course"],
                student["year_level"],
                student["section"]
            )

            if schedule:

                status = mark_attendance(
                    student["id_number"],
                    schedule["course_code"],
                    schedule["room_name"]
                )

            else:

                status = "No Schedule"

        else:

            status = "Student Not Found"

    # Display ID Number
    if id_number:

        cv2.putText(
            frame,
            f"ID: {id_number}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    # Display Student Information
    if student:

        cv2.putText(
            frame,
            f"{student['first_name']} {student['last_name']}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            status,
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("Student ID Scanner", frame)

    key = cv2.waitKey(1)

    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()