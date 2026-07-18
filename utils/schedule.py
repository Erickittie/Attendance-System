from utils.database import get_connection
from datetime import datetime

def get_current_schedule(program, year_level, section):

    today = datetime.now().strftime("%A")
    now = datetime.now().strftime("%H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM class_schedule
        WHERE
            program=%s
            AND year_level=%s
            AND section=%s
            AND day_of_week=%s
            AND start_time<=%s
            AND end_time>=%s
        LIMIT 1
    """,
    (
        program,
        year_level,
        section,
        today,
        now,
        now
    ))

    schedule = cursor.fetchone()

    cursor.close()
    conn.close()

    return schedule