from flask import jsonify
from scanner import latest_scan, start_scanner
from flask import Flask, render_template, request, redirect, url_for, send_file
from utils.database import get_connection
from utils.student import get_student
from utils.schedule import get_current_schedule
from utils.attendance import mark_attendance
from utils.csv_export import export_attendance
from flask import Response
from camera_stream import generate_frames

app = Flask(__name__)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("home.html")


# ==========================================
# REGISTER STUDENT
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        id_number = request.form["id_number"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        course = request.form["course"]
        year_level = request.form["year_level"]
        section = request.form["section"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (
                id_number,
                first_name,
                last_name,
                course,
                year_level,
                section
            )
            VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            id_number,
            first_name,
            last_name,
            course,
            year_level,
            section
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("register"))

    return render_template("register.html")


# ==========================================
# ATTENDANCE PAGE
# ==========================================

@app.route("/attendance")
def attendance():
    return render_template("attendance.html")


# ==========================================
# SCAN STUDENT ID
# ==========================================

@app.route("/scan", methods=["POST"])
def scan():

    id_number = request.form["id_number"]

    student = get_student(id_number)

    if student is None:
        return "Student not found."

    schedule = get_current_schedule(
        student["course"],
        student["year_level"],
        student["section"]
    )

    if schedule is None:
        return "No active schedule found."

    success = mark_attendance(
        student["id_number"],
        schedule["course_code"],
        schedule["room_name"]
    )

    if success:
        status = "Present"
    else:
        status = "Already Recorded"

    return render_template(
        "result.html",
        student=student,
        schedule=schedule,
        status=status
    )


# ==========================================
# ATTENDANCE HISTORY
# ==========================================

@app.route("/history")
def history():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            attendance.*,
            students.first_name,
            students.last_name
        FROM attendance

        JOIN students

        ON attendance.id_number = students.id_number

        ORDER BY attendance.attendance_date DESC,
                 attendance.time_in DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "history.html",
        records=records
    )


# ==========================================
# EXPORT CSV
# ==========================================

@app.route("/export")
def export():

    filename = export_attendance()

    return send_file(
        filename,
        as_attachment=True
    )

@app.route("/schedule/add", methods=["POST"])
def add_schedule():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO class_schedule
        (
            course_code,
            course_name,
            program,
            year_level,
            section,
            room_name,
            day_of_week,
            start_time,
            end_time,
            instructor
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        request.form["course_code"],
        request.form["course_name"],
        request.form["program"],
        request.form["year_level"],
        request.form["section"],
        request.form["room_name"],
        request.form["day_of_week"],
        request.form["start_time"],
        request.form["end_time"],
        request.form["instructor"]
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/schedule")

@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route("/scanner/status")
def scanner_status():

    return jsonify(latest_scan)

# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)