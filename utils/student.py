from database import get_connection


def get_student(id_number):

    db = get_connection()
    cursor = db.cursor(dictionary=True)


    cursor.execute("""
        SELECT
            student_id,
            id_number,
            first_name,
            last_name
        FROM students
        WHERE id_number = %s
    """, (id_number,))


    student = cursor.fetchone()


    cursor.close()
    db.close()


    return student