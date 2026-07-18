from utils.database import get_connection

def get_student(id_number):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM students
        WHERE id_number=%s
    """,(id_number,))

    student = cursor.fetchone()

    cursor.close()
    conn.close()

    return student