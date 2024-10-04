import cv2
import warnings

def process_frame(frame, model):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run model

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        results = model(img)

    # Get result as DataFrame
    df = results.pandas().xyxy[0]

    is_detected = False

    if df.empty:
        return frame, is_detected, 0, 0, 0, 0

    # Get the width of the frame
    frame_width = frame.shape[1]
    frame_mid_x = frame_width // 2  # Screen midpoint (x-axis)

    x_pixel = 0
    y_pixel = 0
    h_pixel = 0
    w_pixel = 0

    df["area"] = (df["xmax"] - df["xmin"]) * (df["ymax"] - df["ymin"])

    largest = df.loc[df["area"].idxmax()]

    confidence = largest["confidence"]

    if confidence < 0.1:
        return frame, is_detected, 0, 0, 0, 0

    # Coordinates
    x_min = int(largest["xmin"])
    y_min = int(largest["ymin"])
    x_max = int(largest["xmax"])
    y_max = int(largest["ymax"])

    # Draw rectangle
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # Calculate the midpoint of the rectangle
    x_mid = (x_min + x_max) // 2
    y_mid = (y_min + y_max) // 2
    h_pixel = y_max - y_min
    w_pixel = x_max - x_min

    # Draw a red dot at the center of the rectangle
    cv2.circle(frame, (x_mid, y_mid), 5, (0, 0, 255), -1)

    # If the rectangle's center is close to the middle of the frame, set "True"
    if abs(x_pixel - frame_mid_x) < 10000:  # 50 pixel proximity tolerance
        is_detected = True

    return frame, is_detected, x_min, y_min, w_pixel, h_pixel
