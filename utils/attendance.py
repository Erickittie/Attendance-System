from database import get_connection

from datetime import datetime



def mark_attendance(student_id, schedule_id):


    db = get_connection()

    cursor = db.cursor()



    # prevent duplicate attendance

    cursor.execute("""

        SELECT attendance_id

        FROM attendance

        WHERE student_id=%s

        AND schedule_id=%s

        AND attendance_date=CURDATE()

    """,
    (
        student_id,
        schedule_id
    ))



    existing = cursor.fetchone()



    if existing:

        cursor.close()

        db.close()

        return False



    # insert attendance

    cursor.execute("""

        INSERT INTO attendance

        (
            student_id,

            schedule_id,

            attendance_date,

            time_in,

            status

        )


        VALUES

        (

            %s,

            %s,

            CURDATE(),

            CURTIME(),

            'Present'

        )

    """,
    (
        student_id,

        schedule_id

    ))



    db.commit()



    cursor.close()

    db.close()



    return True