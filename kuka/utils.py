import math

def calculate_base(angle_degrees, height):
    
    angle_radians = math.radians(angle_degrees)
    base = height / math.tan(angle_radians)
    
    return base

def pixels2mm(x_pixel, y_pixel, w_pixel, h_pixel, x_pos_mm = 1250, y_pos_mm = 550, z_pos_mm = 2500):
    base_pos = {"x": x_pos_mm, "y": y_pos_mm, "z": z_pos_mm}
    # camera resolution 1080/1920
    # camera verticle angle 85, horizontal 50
    v_ang = 42.5
    h_ang = 25

    w_mm = calculate_base(v_ang, base_pos["z"])
    h_mm = calculate_base(h_ang, base_pos["z"])

    # print(f"{x_width}   {y_width}")

    x_obj_mid = x_pixel + w_pixel/2
    y_obj_mid = y_pixel + h_pixel/2
    
    x_ratio = (x_obj_mid/1920)*2
    y_ratio = (y_obj_mid/1080)*2

    if x_ratio > 1:
        x_ratio -= 1
    elif x_ratio < 1:
        x_ratio = x_ratio - 1
    else:
        x_ratio = 0
    

    if y_ratio > 1:
        y_ratio -= 2
    elif y_ratio < 1:
        y_ratio = 1 - x_ratio
    else:
        y_ratio = 0

    x_delta = w_mm*x_ratio
    y_delta = h_mm*y_ratio

    x_mm = base_pos["x"] + x_delta
    y_mm = base_pos["y"] + y_delta

    return x_mm, y_mm, w_mm, h_mm

def width2angle(w_mm, l=10):
    w_cm = w_mm / 10
    rad = 2 * math.asin(w_cm/ (2*l))    # radians
    angle = math.degrees(rad)             # degrees
    return angle
    