import pantilthat
import numpy

# Max degrees the camera can turn
MAX_DEGREES = 80
# Max degrees the camera should turn in a frame
MAX_MOVE_SPEED = 10


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


def get_position():
    pan = pantilthat.get_pan()
    tilt = pantilthat.get_tilt()
    return (pan, tilt)

def set_camera(direction, degrees):
    degrees = clamp(degrees)

    if direction == "pan":
        pantilthat.pan(degrees)
    elif direction == "tilt":
        pantilthat.tilt(degrees)

def move_camera(pan, tilt):
    set_camera("pan", pan)
    set_camera("tilt", tilt)

def change_pan(degrees):
    set_camera("pan", pantilthat.get_pan() + degrees)

def chagne_tilt(degrees):
    set_camera("tilt", pantilthat.get_tilt() + degrees)

def change_camera(x, y):
    change_pan(x)
    change_tilt(y)

def move_towards(frame, shapes):
    if len(shapes) == 0:
        return frame

    # Use first shape
    (left_x, left_y, w, h) = shapes[0]
    # Get center
    (x, y) = (left_x + w / 2, left_y + h / 2)
    (x, y) = normalize_coordinates(frame, x, y)
    (x, y) = coordinates_to_degrees(x, y)

    # Move camera
    change_camera(x, y)


def reset_position():
    move_camera(0, -45)

