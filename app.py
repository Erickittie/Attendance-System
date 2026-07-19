from flask import Flask, render_template

from routes.student_course import student_course_bp
from routes.student_scan import student_scan_bp
from routes.teacher import teacher_bp



app = Flask(__name__)



app.register_blueprint(
    student_course_bp,
    url_prefix="/student"
)



app.register_blueprint(
    student_scan_bp,
    url_prefix="/student"
)



app.register_blueprint(
    teacher_bp
)




@app.route("/")
def home():

    return render_template(
        "home.html"
    )




if __name__ == "__main__":

    app.run(
        debug=True
    )