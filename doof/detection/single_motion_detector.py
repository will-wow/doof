# import the necessary packages
import numpy as np
import imutils
import cv2

# A weight factor
ACCUM_WEIGHT = 0.1
# Minimum frames to do a change detection
MIN_FRAME_COUNT = 2
# Threshold for detecting movement
THRESHOLD = 25

def simplify_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    return gray

def is_whole_frame(frame, motion):
    (minX, minY, maxX, maxY) = motion
    height, width, _ = frame.shape
    movement_height = maxY - minY
    movement_width = maxX - minX

    image_area = width * height
    movement_area = movement_width * movement_height

    return movement_area >= image_area * 0.95

def highlight_movement(frame, motion):
    (minX, minY, maxX, maxY) = motion
    # Draw box
    return cv2.rectangle(frame, (minX, minY), (maxX, maxY), (0, 0, 255), 2) 



class SingleMotionDetector:
    def __init__(self):
        # initialize the background model
        self.bg = None
        self.frame_count = 0

    def reset(self):
        self.frame_count = 0
        self.bg = None

    def detect_bop(self, frame):
        gray = simplify_image(frame)

        bopped = False

        # Look for a bop
        if self.frame_count >= MIN_FRAME_COUNT:
            motion = self.detect(gray)

            if motion is not None:
                bopped = is_whole_frame(frame, motion)
                frame = highlight_movement(frame, motion)

        # Update the model with the new frame
        self.update(gray)

        return (frame, bopped)

    def update(self, frame):
        # Initialize the background model
        if self.bg is None:
            self.bg = frame.copy().astype("float")
            return

        # update the background by accumulating the average
        # If this spikes, then there is motion.
        cv2.accumulateWeighted(frame, self.bg, ACCUM_WEIGHT)
        self.frame_count += 1

    def detect(self, frame):
        delta = cv2.absdiff(self.bg.astype("uint8"), frame)
        thresh = cv2.threshold(delta, THRESHOLD, 255, cv2.THRESH_BINARY)[1]

        # remove small blobs
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # find contours in the thresholded image and initialize the
        # minimum and maximum bounding box regions for motion
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        # if no contours were found, return None
        if len(cnts) == 0:
            return None

        # otherwise, loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and use it to
            # update the minimum and maximum bounding box regions
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))

        # otherwise, return a tuple of the bounding box
        return (minX, minY, maxX, maxY)
    
