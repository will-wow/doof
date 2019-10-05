import time
import threading
import pantilthat
import imutils
import cv2

from doof.detection.face_detector import detect_faces, highlight_faces
from doof.move import reset_position, move_towards

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
searching = False

def shrink_image(frame):
    frame = imutils.resize(frame, width=400)
    frame = cv2.flip(frame, 0)
    return frame

class Brain:
    def __init__(self, video_stream):
        # initialize the video stream
        self.vs = video_stream
        # allow the camera sensor to warm up
        time.sleep(2.0)

        self.outputFrame = None

        # a lock used to ensure thread-safe exchanges of the output frames
        # (useful when multiple browsers/tabs are viewing the stream)
        self.lock = threading.Lock()

        self.searching = False

    def run(self):
        reset_position()

        while True:
            frame = self.vs.read()
            frame = shrink_image(frame)

            faces = detect_faces(frame)
            move_towards(frame, faces)
            frame = highlight_faces(frame, faces)

            # Save the output in a lock, so this doesn't happen while serving a frame
            with self.lock:
                self.outputFrame = frame.copy()

