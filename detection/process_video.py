import cv2
from PIL import Image, ImageTk

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
    for _, row in df.iterrows():
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

def update_frame(cap, panel):
    
    _, frame = cap.read()

    # Process the frame with YOLOv5
    processed_frame, is_mid = process_frame(frame, panel.model)

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

    panel.label_img.img_tk = img_tk
    panel.label_img.configure(image=img_tk)

    panel.label_img.after(10, update_frame, cap, panel)
     



