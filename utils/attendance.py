from datetime import datetime
from utils.database import get_connection

def mark_attendance(id_number, course_code, room_name):

    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().date()
    now = datetime.now().time()

    # Prevent duplicate attendance for the same class on the same day
    cursor.execute("""
        SELECT attendance_id
        FROM attendance
        WHERE id_number=%s
        AND course_code=%s
        AND attendance_date=%s
    """, (id_number, course_code, today))

    existing = cursor.fetchone()

    if existing:
        cursor.close()
        conn.close()
        return False

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
        (
            %s,%s,%s,%s,%s,%s
        )
    """,
    (
        id_number,
        course_code,
        room_name,
        today,
        now,
        "Present"
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return True