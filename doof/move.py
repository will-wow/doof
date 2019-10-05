import pantilthat

def normalize_coordinates(frame, x, y):
    height, width, _ = frame.shape
    midX = width / 2
    midY = height / 2
    return (
        (x - midX) / midX,
        (y - midY) / midY
    )

def move_towards(frame, shapes):
    if len(shapes) == 0:
        return frame

    (left_x, left_y, w, h) = shapes[0]
    (x, y) = (left_x + w//2, left_y + h//2)
    (x, y) = normalize_coordinates(frame, x, y)

    if x > 0.1:
        pan = pantilthat.get_pan()
        if pan <= 80:
            pantilthat.pan(pan + 5)
    if x < -0.1:
        pan = pantilthat.get_pan()
        if pan >= -80:
            pantilthat.pan(pan - 5)
    if y > 0.1:
        tilt = pantilthat.get_tilt()
        if tilt <= 80:
            pantilthat.tilt(tilt + 5)
    if x < -0.1:
        tilt = pantilthat.get_tilt()
        if tilt >= -80:
            pantilthat.tilt(tilt - 5)

def reset_position():
    pantilthat.pan(0)
    pantilthat.tilt(-45)
