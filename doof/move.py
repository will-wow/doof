import time
import pantilthat
import numpy

# Max degrees the camera can turn
MAX_DEGREES = 80
# Max degrees the camera should turn in a frame
MAX_MOVE_SPEED = 10

# Seconds it probably takes to do a move
MOVE_TIME = 2

def normalize_coordinates(frame, x, y):
    height, width, _ = frame.shape
    midX = width / 2
    midY = height / 2
    return ((x - midX) / midX, (y - midY) / midY)


def coordinates_to_degrees(x, y):
    # Moves more slowly the closer the face is to the center.
    return (x * MAX_MOVE_SPEED, y * MAX_MOVE_SPEED)


def clamp(value):
    return numpy.clip(int(value), -MAX_DEGREES, MAX_DEGREES)


class Move:
    def __init__(self, pantilthat=pantilthat):
        self.pantilthat = pantilthat

        self.last_move = time.time()


    def get_position(self):
        pan = self.pantilthat.get_pan()
        tilt = self.pantilthat.get_tilt()
        return (pan, tilt)

    def set_camera(self, direction, degrees):
        degrees = clamp(degrees)

        if direction == "pan":
            self.pantilthat.pan(degrees)
        elif direction == "tilt":
            self.pantilthat.tilt(degrees)

        self.last_move = time.time()

    def is_moving(self):
        return self.last_move > time.time() - MOVE_TIME

    def move_camera(self, pan, tilt):
        self.set_camera("pan", pan)
        self.set_camera("tilt", tilt)

    def change_pan(self, degrees):
        self.set_camera("pan", self.pantilthat.get_pan() + degrees)

    def change_tilt(self, degrees):
        self.set_camera("tilt", self.pantilthat.get_tilt() + degrees)

    def change_camera(self, x, y):
        self.change_pan(x)
        self.change_tilt(y)

    def move_towards(self, frame, shape):
        # Use first shape
        (left_x, left_y, w, h) = shape
        # Get center
        (x, y) = (left_x + w / 2, left_y + h / 2)
        (x, y) = normalize_coordinates(frame, x, y)
        (x, y) = coordinates_to_degrees(x, y)

        # Move camera
        self.change_camera(x, y)


    def reset_position(self):
        self.move_camera(0, -45)

