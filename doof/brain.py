import time
import threading
import imutils
import cv2

from doof.detection.face_detector import detect_faces, highlight_faces
from doof.detection.single_motion_detector import SingleMotionDetector
from doof.sleep import Sleep
from doof.move import Move

BORED_TIME = 15

def shrink_image(frame):
    frame = imutils.resize(frame, width=400)
    frame = cv2.flip(frame, 0)
    return frame


class Brain:
    def __init__(
        self, 
        video_stream,
        move = None,
        sleep = None,
        md = None
    ):
        self.vs = video_stream
        self.move = move or Move()
        self.sleep = sleep or Sleep(self.move)
        self.md = SingleMotionDetector()

        # allow the camera sensor to warm up
        time.sleep(2.0)

        self.outputFrame = None

        # a lock used to ensure thread-safe exchanges of the output frames
        # (useful when multiple browsers/tabs are viewing the stream)
        self.lock = threading.Lock()

        self.searching = False

    def handle_faces(self, frame):
        if self.sleep.sleeping:
            return frame

        faces = detect_faces(frame)
        frame = highlight_faces(frame, faces)

        if len(faces):
            self.move.move_towards(frame, faces[0])

        return frame

    def handle_bordem(self):
        if self.move.last_move < time.time() - BORED_TIME:
            self.sleep.sleep()


    def handle_bop(self, frame):
        (frame, bop) = self.md.detect_bop(frame, self.move.is_moving())

        if bop:
            self.sleep.bop()

        return frame

    def run(self):
        self.sleep.wake()

        while True:
            frame = self.vs.read()
            frame = shrink_image(frame)

            frame = self.handle_faces(frame)
            frame = self.handle_bop(frame)
            self.handle_bordem()


            # Save the output in a lock, so this doesn't happen while serving a frame
            with self.lock:
                self.outputFrame = frame.copy()

