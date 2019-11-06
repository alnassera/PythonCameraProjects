from flask import Response
from flask import Flask
from flask import render_template
import color_test
import cv2
import numpy as np
import runtime, greenlet

# initialize a flask object
app = Flask(__name__)


GREEN_THRESHOLD_LOW = (36, 25, 25)
GREEN_THRESHOLD_HIGH = (86, 255, 255)

RED_THRESHOLD_LOW_1 = np.array([0, 120, 70])
RED_THRESHOLD_HIGH_1 = np.array([10,255, 255])
RED_THRESHOLD_LOW_2 = np.array([0, 120, 70])
RED_THRESHOLD_HIGH_2 = np.array([10,255, 255])


CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

MIN_RADIUS = 2

cam = cv2.VideoCapture(0)

print("Camera initialized")
iterator = 0
iterator_1 = 0
first_pt = None
second_pt = None
has_Green = False


global img
global ret_val
ret_val, img = cam.read()
img = cv2.flip(img, 1)

@app.route("/")
def index():
    # return the rendered template
    return render_template("welcome.html")


def generate():
    while True:
        color_test.pen(iterator, iterator_1, first_pt, second_pt, has_Green, img, ret_val)
    while True:
        print("ERROR")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def clear_all():
    ret_val, img = cam.read()
    return img.tobytes()


# check to see if this is the main thread of execution

if __name__ == '__main__':

    app.run(debug=True,
            threaded=True, use_reloader=False)

