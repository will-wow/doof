import time
import pantilthat
import numpy

# Max degrees the camera can turn
MAX_DEGREES = 80
# Max degrees the camera should turn in a frame
MAX_MOVE_SPEED = 10

# Time to do any move
MOVE_TIME = 0.5

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
    def __init__(self, pantilthat=pantilthat, md=None):
        self.pantilthat = pantilthat
        self.md = md

        self.move_complete_at = time.time()
        
        self.pan = self.pantilthat.get_pan()
        self.tilt = self.pantilthat.get_tilt()


    def get_both(self):
        return (self.pan, self.tilt)

    def get_one(self, direction):
        if direction == "pan":
            return self.pan
        else:
            return self.tilt

    def move_one(self, direction, degrees):
        self.move_complete_at = time.time() + MOVE_TIME
        self.md.reset()

        return self._set_one(direction, degrees)

    def move_both(self, pan, tilt):
        self.move_complete_at = time.time() + MOVE_TIME
        self.md.reset()

        return self._set_both(pan, tilt)

    def change_one(self, direction, degrees):
        return self.move_one(direction, self.get_one(direction) + degrees)

    def change_both(self, pan, tilt):
        return self.move_both(self.pan + pan, self.tilt + tilt)

    def move_towards(self, frame, shape):
        # Use first shape
        (left_x, left_y, w, h) = shape
        # Get center
        (x, y) = (left_x + w / 2, left_y + h / 2)
        (x, y) = normalize_coordinates(frame, x, y)
        (x, y) = coordinates_to_degrees(x, y)

        # Move camera
        return self.change_both(x, y)

    def reset_position(self):
        self.move_both(0, -45)

    def is_moving(self):
        return self.move_complete_at >= time.time()

    def _set_one(self, direction, degrees):
        degrees = int(degrees)

        # Return false if can't move anymore
        if degrees < -MAX_DEGREES:
            return False
        if degrees > MAX_DEGREES:
            return False

        if direction == "pan":
            self.pan = degrees
            self.pantilthat.pan(degrees)
        elif direction == "tilt":
            self.tilt = degrees
            self.pantilthat.tilt(degrees)

        return True

    def _set_both(self, pan, tilt):
        self._set_one("pan", pan)
        self._set_one("tilt", tilt)

