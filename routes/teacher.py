from flask import Blueprint, render_template, request, send_file
from database import get_connection

import csv
import os
from datetime import datetime



teacher_bp = Blueprint(
    "teacher",
    __name__
)



# ==========================================
# TEACHER DASHBOARD
# SELECT CLASS SCHEDULE
# ==========================================

@teacher_bp.route("/teacher")
def teacher_dashboard():


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


        ORDER BY cs.day_of_week,
        cs.start_time

    """)



    schedules = cursor.fetchall()



    cursor.close()
    db.close()



    return render_template(
        "teacher_dashboard.html",
        schedules=schedules
    )





# ==========================================
# VIEW ATTENDANCE
# ==========================================

@teacher_bp.route(
    "/teacher/attendance"
)
def teacher_attendance():


    schedule_id = request.args.get(
        "schedule_id"
    )


    db = get_connection()

    cursor = db.cursor(dictionary=True)



    # GET SCHEDULE INFO

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




    # GET ATTENDANCE


    cursor.execute("""
        SELECT


            s.id_number,


            CONCAT(

                s.first_name,

                ' ',

                s.last_name

            ) AS name,


            a.status,


            a.time_in


        FROM attendance a



        INNER JOIN students s


        ON a.student_id=s.student_id



        WHERE a.schedule_id=%s



        AND a.attendance_date=CURDATE()


    """,
    (
        schedule_id,
    ))



    attendance = cursor.fetchall()



    cursor.close()

    db.close()



    return render_template(

        "teacher_attendance.html",

        schedule=schedule,

        attendance=attendance

    )





# ==========================================
# EXPORT CSV
# ==========================================

@teacher_bp.route(
    "/teacher/export"
)
def export_csv():


    schedule_id = request.args.get(
        "schedule_id"
    )



    db=get_connection()

    cursor=db.cursor(dictionary=True)



    cursor.execute("""
        SELECT


            s.id_number,


            CONCAT(

                s.first_name,

                ' ',

                s.last_name

            ) AS name,


            a.status,


            a.time_in


        FROM attendance a


        INNER JOIN students s


        ON a.student_id=s.student_id



        WHERE a.schedule_id=%s


        AND a.attendance_date=CURDATE()

    """,
    (
        schedule_id,
    ))



    rows = cursor.fetchall()



    cursor.close()

    db.close()



    filename = (

        "attendance_"

        +

        datetime.now()
        .strftime("%Y%m%d_%H%M%S")

        +

        ".csv"

    )



    filepath = os.path.join(

        "static",

        filename

    )



    with open(

        filepath,

        "w",

        newline=""

    ) as file:



        writer = csv.writer(file)



        writer.writerow([

            "ID Number",

            "Student Name",

            "Status",

            "Time In"

        ])




        for row in rows:


            writer.writerow([

                row["id_number"],

                row["name"],

                row["status"],

                row["time_in"]

            ])




    return send_file(

        filepath,

        as_attachment=True

    )