import cv2
import time
from datetime import datetime

from utils.ocr import detect_id_number
from utils.student import get_student
from utils.schedule import get_current_schedule
from utils.attendance import mark_attendance


camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Cannot open camera")
    exit()


# ==============================
# VARIABLES
# ==============================

last_id = ""
last_scan_time = 0

student = None
schedule = None
status = ""


latest_scan = {
    "id_number": "",
    "name": "",
    "course": "",
    "room": "",
    "status": "",
    "time": ""
}


# ==============================
# SCANNING FUNCTION
# ==============================

def process_scan(id_number):

    global student
    global schedule
    global status


    # Get student information
    student = get_student(id_number)


    # Get current schedule
    schedule = get_current_schedule()


    print("Student:", student)
    print("Schedule:", schedule)


    # Check if data exists
    if student and schedule:


        try:

            success = mark_attendance(
                student["id_number"],
                schedule["course_code"],
                schedule["room_name"]
            )


            status = "Present" if success else "Already Recorded"


            latest_scan.update({

                "id_number": student.get("id_number"),

                "name":
                    f'{student.get("first_name","")} '
                    f'{student.get("last_name","")}',

                "course":
                    schedule.get("course_code"),

                "room":
                    schedule.get("room_name"),

                "status":
                    status,

                "time":
                    datetime.now().strftime("%I:%M:%S %p")

            })


            print(latest_scan)


        except Exception as e:

            print("Attendance error:", e)



    else:


        if student is None:

            print("Student not found")

            latest_scan["status"] = "Student Not Found"


        elif schedule is None:

            print("No active schedule")

            latest_scan["status"] = "No Schedule"



    return latest_scan

# ==============================
# CAMERA SCANNER LOOP
# ==============================

def start_scanner():

    global last_id
    global last_scan_time


    while True:

        ret, frame = camera.read()

        if not ret:
            continue


        # Detect ID number using OCR
        detected_id = detect_id_number(frame)


        if detected_id:

            print("Detected ID:", detected_id)


            # Avoid duplicate scanning
            if detected_id != last_id or time.time() - last_scan_time > 5:


                last_id = detected_id
                last_scan_time = time.time()


                # Send ID to your existing function
                process_scan(detected_id)


        # Optional: show camera
        cv2.imshow(
            "Attendance Scanner",
            frame
        )


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    camera.release()
    cv2.destroyAllWindows()