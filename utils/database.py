import mysql.connector
from config import *

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="erick123",
        database="attendance_db"
    )