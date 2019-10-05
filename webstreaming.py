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

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0

    while True
        # read the next frame, resize smaller, grayscale and blur (less noise)
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
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
                cv2.rectangle(frame, (mixX, minY), (maxX, maxY),
                              (0, 0, 255), 2)

            # update the model
            md.update(gray)
            total += 1

            with lock:
                outputFrame = frame.copy()


        
        


