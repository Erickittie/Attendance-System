from flask import Blueprint, Response
from utils.camera import generate_frames


camera_bp = Blueprint(
    "camera",
    __name__
)


@camera_bp.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(),
        mimetype=
        "multipart/x-mixed-replace; boundary=frame"
    )