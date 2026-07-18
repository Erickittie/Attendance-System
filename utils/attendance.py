from datetime import date, datetime
from utils.database import get_connection


def already_attended(id_number, course_code):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE id_number = %s
        AND course_code = %s
        AND attendance_date = %s
    """,
    (
        id_number,
        course_code,
        date.today()
    ))

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count > 0


def mark_attendance(id_number, course_code, room_name):

    if already_attended(id_number, course_code):
        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance
        (
            id_number,
            course_code,
            room_name,
            attendance_date,
            time_in,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s)
    """,
    (
        id_number,
        course_code,
        room_name,
        date.today(),
        datetime.now().strftime("%H:%M:%S"),
        "Present"
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return True