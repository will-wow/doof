from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import cv2

from doof.brain import Brain

# ==========
# Brain
# ==========

vs = VideoStream(usePiCamera=1).start()
brain = Brain(vs)


def start_brain():
    brain.run()


# ==========
# Web Server
# ==========

IP = "0.0.0.0"
PORT = 8000
DEBUG = True

# initialize a flask object
app = Flask(__name__)


def generate_frame():
    with brain.lock:
        outputFrame = brain.outputFrame

        if outputFrame is None:
            return None

        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

        # ensure the frame was successfully encoded
        if not flag:
            return None

    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) +
            b'\r\n')


def generate():
    while True:
        data = generate_frame()

        if data is None:
            continue

        yield (data)


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# ==========
# Start
# ==========

# check to see if this is the main thread of execution
if __name__ == '__main__':
    # start a thread that will run the brain.
    t = threading.Thread(target=start_brain)
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=IP, port=PORT, debug=DEBUG, threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()
