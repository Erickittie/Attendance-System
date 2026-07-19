from flask import Blueprint, render_template, request, redirect, url_for

from database import get_connection


student_course_bp = Blueprint(
    "student_course",
    __name__
)



@student_course_bp.route("/")
def select_course():


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

    """)


    schedules = cursor.fetchall()


    cursor.close()
    db.close()



    return render_template(
        "student_course.html",
        schedules=schedules
    )





@student_course_bp.route(
    "/select",
    methods=["POST"]
)
def process_course():


    schedule_id = request.form["schedule_id"]



    return redirect(

        url_for(

            "student_scan.scan_page",

            schedule_id=schedule_id

        )

    )