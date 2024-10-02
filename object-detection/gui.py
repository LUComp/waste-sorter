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
        self.geometry("800x600")                #set size of main window

        self.label_img = tk.Label()
        self.label_img.pack()

        self.takephoto_button = tk.Button(self, text="", command = self.example)
        self.takephoto_button.pack()

        self.audiocall_button = tk.Button(self, text="", command = self.example)
        self.audiocall_button.pack()

    def example():
        return
    
    def process_frame(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run model
        results = model(img)

        # Get result as DataFrame
        df = results.pandas().xyxy[0]

        # Loop for detected objects
        for index, row in df.iterrows():
            # Coordinates
            x_min = int(row['xmin'])
            y_min = int(row['ymin'])
            x_max = int(row['xmax'])
            y_max = int(row['ymax'])

            # Draw rectangle
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        return frame
    
    def update_frame(self):
        # Capture frame from the webcam
        ret, frame = cap.read()

        if ret:
            # Process the frame with YOLOv5
            processed_frame = self.process_frame(frame)

            # Convert processed frame (BGR) to PIL Image (RGB)
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(processed_frame)

            # Resize the image to fit the label size (600x400 in this case)
            img_pil_resized = img_pil.resize((600, 400), )

            img_tk = ImageTk.PhotoImage(image=img_pil_resized)

            # Update the tkinter label with the new frame
            self.label_img.config(image=img_tk)
            self.label_img.image = img_tk

        # Schedule the next frame update (16 ms corresponds to ~60 FPS)
        self.after(16, self.update_frame)

        # Create mask
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_green = np.array([40, 40, 40])  # Bottom green border
        upper_green = np.array([80, 255, 255])  # Top green border
        mask = cv2.inRange(hsv, lower_green, upper_green)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # Filter for large contours
            area = cv2.contourArea(contour)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(contour)
        return (x, y), h, w

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













    