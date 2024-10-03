import math

def pixels2mm(x, y, h, w):
    return 0, 0, 0, 0

def width2angle(w_mm, l=10):
    w_cm = w_mm / 10
    rad = 2 * math.asin(w_cm/ (2*l))    # radians
    angle = math.degrees(rad)             # degrees
    return angle
    