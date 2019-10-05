# import the necessary packages
from pyimagesearch.motion_detection import SingleMotionDetector
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

def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock


    pantilthat.pan(0)
    pantilthat.tilt(0)

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0

    while True:
        # read the next frame, resize smaller, grayscale and blur (less noise)
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        frame = cv2.flip(frame, 0)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # grab the timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(
            frame,
            timestamp.strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.35,
            (0, 0, 255),
            1
        )

        # If there are enough frames to do detection
        if total > frameCount:
            motion = md.detect(gray)

            if motion is not None:
                # Destructure data
                (thresh, (minX, minY, maxX, maxY)) = motion
                # Draw box
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                              (0, 0, 255), 2)

                height, width, _ = frame.shape
                midX = width / 2
                midY = height / 2
                x = ((maxX + minX) / 2)
                y = ((maxY + minY) / 2)
                move(
                    (x - midX) / midX,
                    (y - midY) / midY
                )

        # update the model
        md.update(gray)
        total += 1

        with lock:
            outputFrame = frame.copy()

def move(x, y):
    if x > 10:
        pan = pantilthat.get_pan()
        if pan <= 80:
            pantilthat.pan(pan + 5)
    if x < 10:
        pan = pantilthat.get_pan()
        if pan >= -80:
            pantilthat.pan(pan - 5)
    if y > 10:
        tilt = pantilthat.get_tilt()
        if tilt <= 80:
            pantilthat.tilt(tilt + 5)
    if x < 10:
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
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, default=8000,
        help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
        help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
        threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()

