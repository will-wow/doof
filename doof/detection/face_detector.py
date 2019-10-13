# import the necessary packages
import numpy as np
import imutils
import cv2

face_cascade = "/home/pi/repos/doof/data/haarcascade_frontalface_default.xml"
face_cascade_alt = "/home/pi/repos/doof/data/haarcascade_frontalface_alt.xml"
smile_cascade = "/home/pi/repos/doof/data/haarcascade_smile.xml"
FACE_CASCADE = cv2.CascadeClassifier()

if not FACE_CASCADE.load(face_cascade):
    print('--(!)Error loading face cascade')
    exit(0)


def simplify_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    return gray


def detect_faces(frame):
    frame_gray = simplify_image(frame)
    return FACE_CASCADE.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=3)                                        



def highlight_faces(frame, faces):
    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
        # Draw face circles
        frame = cv2.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360,
                            (255, 0, 255), 4)

    return frame
