import tkinter as tk
import torch
import cv2
import numpy as np
import ssl
from PIL import Image, ImageTk

class CamOptions(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Waste Sorter")        #set title of main window
        self.geometry("1000x600")                #set size of main window
        #self.configure(background="gray")

        # Create a frame to contain the video label
        self.frame_video = tk.Frame(self, width=600, height=400)
        self.frame_video.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Create label for the video inside the frame
        self.label_img = tk.Label(self.frame_video, width=600, height=400)
        self.label_img.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Object-related details
        # Create labels to display width and height

        self.height_label = tk.Label(self, text="Height: ")
        self.height_label.grid(row=1, column=1, padx=10, pady=10)

        self.width_label = tk.Label(self, text="Width: ")
        self.width_label.grid(row=2, column=1, padx=10, pady=10)

        self.x_label = tk.Label(self, text="X: ")
        self.x_label.grid(row=3, column=1, padx=10, pady=10)

        self.y_label = tk.Label(self, text="Y: ")
        self.y_label.grid(row=4, column=1, padx=10, pady=10)

        self.z_label = tk.Label(self, text="Z: ")
        self.z_label.grid(row=5, column=1, padx=10, pady=10)

        # Arm-related details
        # Create labels to display x,y and z positions


        self.height_label = tk.Label(self, text="Height: ")
        self.height_label.grid(row=2, column=1, padx=10, pady=10)


        self.takephoto_button = tk.Button(self, text="Take Photo", command=self.example)
        self.takephoto_button.grid(row=1, column=0, padx=10, pady=10)

    def example():
        return
    
    def process_frame(self, frame):
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
    
    def update_frame(self):
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
        processed_frame, is_mid = self.process_frame(frame)

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

        # Update the tkinter label with the new frame
        self.label_img.config(image=img_tk)
        self.label_img.image = img_tk

        # Schedule the next frame update (16 ms corresponds to ~60 FPS)
        self.after(16, self.update_frame)

    #def set_x_position():


    #def set_y_position():

    def start(self):
        self.mainloop()                                #start tkinter mainloop

if __name__ == "__main__":
    # SSL
    ssl._create_default_https_context = ssl._create_unverified_context

    # YOLOv5
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    cap = cv2.VideoCapture(0)

    comm_options = CamOptions()    #instantiate and start communication options window

    comm_options.update_frame()

    comm_options.start()

    # Release the webcam when the window is closed
    cap.release()
    cv2.destroyAllWindows()













    