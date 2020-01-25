y = (255, 255, 0)  # Yellow
b = (0, 0, 0)  # Black
r = (255, 0, 0) # Red


def show_smiley_face(sense):
    sense.set_pixels([
        y, y, y, y, y, y, y, y,
        y, y, y, y, y, y, y, y,
        y, b, b, y, y, b, b, y,
        y, b, b, y, y, b, b, y,
        y, y, y, y, y, y, y, y,
        y, b, b, y, y, b, b, y,
        y, y, y, b, b, y, y, y,
        y, y, y, y, y, y, y, y
    ])


def show_frowning_face(sense):
    sense.set_pixels([
        r, r, r, r, r, r, r, r,
        r, r, r, r, r, r, r, r,
        r, b, b, r, r, b, b, r,
        r, b, b, r, r, b, b, r,
        r, r, r, r, r, r, r, r,
        r, r, r, b, b, r, r, r,
        r, r, b, r, r, b, r, r,
        r, b, r, r, r, r, b, r
    ])
