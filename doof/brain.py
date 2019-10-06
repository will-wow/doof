import time
import threading
import imutils
import cv2

from doof.detection.face_detector import detect_faces, highlight_faces

def shrink_image(frame):
    frame = imutils.resize(frame, width=400)
    frame = cv2.flip(frame, 0)
    return frame


class Brain:
    def __init__(self, video_stream, move):
        self.vs = video_stream
        self.move = move

        # allow the camera sensor to warm up
        time.sleep(2.0)

        self.outputFrame = None

        # a lock used to ensure thread-safe exchanges of the output frames
        # (useful when multiple browsers/tabs are viewing the stream)
        self.lock = threading.Lock()

        self.searching = False

    def handle_faces(self, frame):
        faces = detect_faces(frame)
        self.move.move_towards(frame, faces)
        frame = highlight_faces(frame, faces)


    def run(self):
        self.move.reset_position()

        while True:
            frame = self.vs.read()
            frame = shrink_image(frame)

            self.handle_faces(frame)

            # Save the output in a lock, so this doesn't happen while serving a frame
            with self.lock:
                self.outputFrame = frame.copy()
