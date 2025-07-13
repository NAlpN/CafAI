from flask import Blueprint, jsonify
import json

camera_dummy = Blueprint('camera_dummy', __name__)

@camera_dummy.route("/dummy-camera")
def dummy_camera():
    with open("camera_data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)