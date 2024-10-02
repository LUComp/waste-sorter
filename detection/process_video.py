import cv2
from PIL import Image, ImageTk
import numpy as np
from main import control_panel, cap, model

def process_frame(frame, model):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run model
    results = model(img)

    # Get result as DataFrame
    df = results.pandas().xyxy[0]

    # Get the width of the frame
    frame_width = frame.shape[1]
    frame_mid_x = frame_width // 2  # Screen midpoint (x-axis)

    # Initialize True/False status
    is_mid = False

    # Loop for detected objects
    for index, row in df.iterrows():
        # Coordinates
        x_min = int(row['xmin'])
        y_min = int(row['ymin'])
        x_max = int(row['xmax'])
        y_max = int(row['ymax'])

        # Draw rectangle
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # Calculate the midpoint of the rectangle
        rect_mid_x = (x_min + x_max) // 2
        rect_mid_y = (y_min + y_max) // 2

        # Draw a red dot at the center of the rectangle
        cv2.circle(frame, (rect_mid_x, rect_mid_y), 5, (0, 0, 255), -1)

        # If the rectangle's center is close to the middle of the frame, set "True"
        if abs(rect_mid_x - frame_mid_x) < 100:  # 50 pixel proximity tolerance
            is_mid = True
        
    return frame, is_mid

def update_frame(cap, model):
    # Capture frame from the webcam
    ret, frame = cap.read()

    if not ret:
        return

    # Create a mask for the green color (in BGR format, green range)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 40, 40])  # Lower green boundary
    upper_green = np.array([80, 255, 255])  # Upper green boundary
    mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # Only take large contours
        area = cv2.contourArea(contour)
        if area > 1000:  # Filter small noises by thresholding area
            # Draw a rectangle around the contour
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Write the coordinates on the corners of the rectangle
            cv2.putText(frame, f"({x},{y})", (x - 50, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
            cv2.putText(frame, f"({x + w},{y})", (x + w + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
            cv2.putText(frame, f"({x},{y + h})", (x - 50, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)
            cv2.putText(frame, f"({x + w},{y + h})", (x + w + 5, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)

            # Write the width and height in the center of the rectangle
            cv2.putText(frame, f"W: {w}", (x + w // 2 - 30, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
            cv2.putText(frame, f"H: {h}", (x - 80, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)

    # Process the frame with YOLOv5
    processed_frame, is_mid = process_frame(frame, model)

    # Write the True/False message in the top left corner
    if is_mid:
        cv2.putText(frame, "True", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    else:
        cv2.putText(frame, "False", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    # Convert processed frame (BGR) to PIL Image (RGB)
    processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(processed_frame)

    # Resize the image to fit the label size (600x400 in this case)
    img_pil_resized = img_pil.resize((600, 400), Image.LANCZOS)

    img_tk = ImageTk.PhotoImage(image=img_pil_resized)

    return img_tk
     



