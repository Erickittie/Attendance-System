from flask import Flask, render_template, request
from utils.database import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Attendance System</h1>

    <a href='/register'>
        Register Student
    </a>
    """

@app.route("/register", methods=["GET","POST"])
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
            (id_number, first_name, last_name, course, year_level, section)

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

        return "Student Registered Successfully!"

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)