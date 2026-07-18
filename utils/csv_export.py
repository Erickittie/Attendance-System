import pandas as pd
import os
from datetime import datetime
from utils.database import get_connection

CSV_FOLDER = "attendance_csv"


def export_attendance():

    if not os.path.exists(CSV_FOLDER):
        os.makedirs(CSV_FOLDER)

    conn = get_connection()

    df = pd.read_sql("""
        SELECT *
        FROM attendance
        ORDER BY attendance_date DESC, time_in DESC
    """, conn)

    filename = os.path.join(
        CSV_FOLDER,
        f"attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    df.to_csv(filename, index=False)

    conn.close()

    return filename