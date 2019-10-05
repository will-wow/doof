import pantilthat
import numpy

# Field of view
X_DEGREES = 62 // 4
Y_DEGREES = 48 // 4
MAX_DEGREES = 80
MIN_DEGREE_MOVE = 8


def normalize_coordinates(frame, x, y):
    height, width, _ = frame.shape
    midX = width / 2
    midY = height / 2
    return ((x - midX) / midX, (y - midY) / midY)


def coordinates_to_degrees(x, y):
    return (int(x * 2.5), int(y * 2.5))


def move_camera(pan, tilt):
    pantilthat.pan(pan)
    pantilthat.tilt(tilt)


def get_position():
    pan = pantilthat.get_pan()
    tilt = pantilthat.get_tilt()
    return (pan, tilt)


def smooth_out_change(old_value, new_value):
    if abs(old_value - new_value) < MIN_DEGREE_MOVE:
        return old_value
    else:
        return new_value


def clamp(value):
    return numpy.clip(value, -MAX_DEGREES, MAX_DEGREES)


def move_towards(frame, shapes):
    if len(shapes) == 0:
        return frame

    (left_x, left_y, w, h) = shapes[0]
    (x, y) = (left_x + w / 2, left_y + h / 2)
    (x, y) = normalize_coordinates(frame, x, y)
    (x, y) = coordinates_to_degrees(x, y)

    (pan, tilt) = get_position()

    new_pan = clamp(pan + x)
    new_tilt = clamp(tilt + y)

    print({
        "pan": pan,
        "tilt": tilt,
        "new_pan": new_pan,
        "new_tilt": new_tilt,
        "x": x,
        "y": y
    })

    new_pan = smooth_out_change(pan, new_pan)
    new_tilt = smooth_out_change(tilt, new_tilt)

    move_camera(new_pan, new_tilt)


def reset_position():
    move_camera(0, -45)


def move_tick(direction):
    if direction == "top":
        value = clamp(pantilthat.get_tilt() - 5)
        pantilthat.tilt(value)
    elif direction == "left":
        value = clamp(pantilthat.get_pan() - 5)
        pantilthat.pan(value)
    if direction == "bottom":
        value = clamp(pantilthat.get_tilt() + 5)
        pantilthat.tilt(value)
    elif direction == "left":
        value = clamp(pantilthat.get_pan() + 5)
        pantilthat.pan(value)
