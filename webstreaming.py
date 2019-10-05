from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
import pantilthat

face_cascade = "data/haarcascade_frontalface_default.xml"
face_cascade_alt = "data/haarcascade_frontalface_alt.xml"
smile_cascade = "data/haarcascade_smile.xml"
FACE_CASCADE = cv2.CascadeClassifier()

if not FACE_CASCADE.load(face_cascade):
    print('--(!)Error loading face cascade')
    exit(0)

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
vs = VideoStream(usePiCamera=1).start()
time.sleep(2.0)

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

def detect_motion():
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock

    pantilthat.pan(0)
    pantilthat.tilt(-45)

    while True:
        # read the next frame, resize smaller, grayscale and blur (less noise)
        frame = vs.read()
        frame = shrink_image(frame)

        frame = detect_faces(frame)

        with lock:
            outputFrame = frame.copy()

def shrink_image(frame):
    frame = imutils.resize(frame, width=400)
    frame = cv2.flip(frame, 0)
    return frame

def simplify_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    return gray

def detect_faces(frame):
    frame_gray = simplify_image(frame)
    faces = FACE_CASCADE.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        # Draw face circles
        frame = cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        # Move towards face
        move_towards(frame, center[0], center[1])

    return frame

def normalize_coordinates(frame, x, y):
    height, width, _ = frame.shape
    midX = width / 2
    midY = height / 2
    return (
        (x - midX) / midX,
        (y - midY) / midY
    )


def move_towards(frame, x, y):
    (x, y) = normalize_coordinates(frame, x, y)

    if x > 0.1:
        pan = pantilthat.get_pan()
        if pan <= 80:
            pantilthat.pan(pan + 5)
    if x < -0.1:
        pan = pantilthat.get_pan()
        if pan >= -80:
            pantilthat.pan(pan - 5)
    if y > 0.1:
        tilt = pantilthat.get_tilt()
        if tilt <= 80:
            pantilthat.tilt(tilt + 5)
    if x < -0.1:
        tilt = pantilthat.get_tilt()
        if tilt >= -80:
            pantilthat.tilt(tilt - 5)

def generate():
    global outputFrame, lock

    while True:
        with lock:
            if outputFrame is None:
                continue

            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype = "multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, default="0.0.0.0",
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, default=8000,
        help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
        help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion)
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
        threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()

