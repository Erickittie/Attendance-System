from flask import Blueprint, render_template, request, jsonify, Response

from database import get_connection

from utils.ocr import detect_id_number
from utils.student import get_student
from utils.attendance import mark_attendance
from utils.camera import get_frame, generate_frames

import cv2



student_scan_bp = Blueprint(
    "student_scan",
    __name__
)



# =====================================
# OPEN SCAN PAGE
# =====================================

@student_scan_bp.route("/scan")
def scan_page():


    schedule_id = request.args.get(
        "schedule_id"
    )


    if not schedule_id:

        return "No schedule selected"



    db = get_connection()

    cursor = db.cursor(dictionary=True)



    cursor.execute("""

        SELECT

            cs.schedule_id,

            c.course_code,

            c.course_name,

            cs.day_of_week,

            cs.start_time,

            cs.end_time,

            cs.room


        FROM class_schedule cs


        INNER JOIN courses c


        ON cs.course_id = c.course_id


        WHERE cs.schedule_id=%s


    """,
    (
        schedule_id,
    ))



    schedule = cursor.fetchone()



    cursor.close()

    db.close()



    return render_template(

        "student_scan.html",

        schedule=schedule,

        schedule_id=schedule_id

    )





# =====================================
# CAMERA STREAM
# =====================================

@student_scan_bp.route("/video_feed")
def video_feed():

    return Response(

        generate_frames(),

        mimetype=
        "multipart/x-mixed-replace; boundary=frame"

    )





# =====================================
# CAPTURE ID
# =====================================

@student_scan_bp.route(
    "/capture",
    methods=["POST"]
)
def capture_id():


    schedule_id = request.args.get(
        "schedule_id"
    )



    if not schedule_id:


        return jsonify({

            "status":"failed",

            "message":
            "No schedule selected"

        })



    frame = get_frame()



    if frame is None:


        return jsonify({

            "status":"failed",

            "message":
            "Camera not ready"

        })




    # SAVE IMAGE

    cv2.imwrite(

        "static/captured.jpg",

        frame

    )




    # OCR

    id_number = detect_id_number(
        frame
    )



    print(
        "Detected ID:",
        id_number
    )




    if not id_number:


        return jsonify({

            "status":"failed",

            "message":
            "ID not detected"

        })




    # FIND STUDENT

    student = get_student(
        id_number
    )



    print(
        "Student:",
        student
    )




    if not student:


        return jsonify({

            "status":"failed",

            "message":
            "Student not registered"

        })





    name = (

        student["first_name"]

        +

        " "

        +

        student["last_name"]

    )




    # SAVE ATTENDANCE

    mark_attendance(

        student["student_id"],

        schedule_id

    )





    return jsonify({

        "status":"success",

        "id_number":
        student["id_number"],


        "name":
        name,


        "attendance":
        "Present"

    })