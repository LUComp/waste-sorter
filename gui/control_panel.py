import tkinter as tk
from PIL import Image, ImageTk
import cv2
from vision.detect import process_frame
from vision.classify import classify_object
from kuka.comms import signal_grip, signal_object
from kuka.kinematics import pixels2mm

class ControlPanel(tk.Tk):

    def __init__(self, title="Waste Sorter"):
        super().__init__()

        self.title("Waste Sorter")        #set title of main window
        self.geometry("1000x600")                #set size of main window
  
        self.create_video_frame()
        self.create_labels()

        self.lock = False
    
    def create_video_frame(self):
        self.frame_video = tk.Frame(self, width=600, height=400)
        self.frame_video.grid(row=0, column=0, padx=10, pady=10)

        self.label_img = tk.Label(self.frame_video, width=600, height=400)
        self.label_img.grid(row=0, column=0, padx=10, pady=10)

    def create_labels(self):
        self.object_label = tk.Label(self, text="Object Details")
        self.object_label.place(x=750, y=50)


        self.object_x_label = tk.Label(self, text="X: ")
        self.object_x_label.place(x=720, y=100)

        self.object_y_label = tk.Label(self, text="Y: ")
        self.object_y_label.place(x=820, y=100)

        self.object_height_label = tk.Label(self, text="Height: ")
        self.object_height_label.place(x=720, y=150)

        self.object_width_label = tk.Label(self, text="Width: ")
        self.object_width_label.place(x=820, y=150)


        self.arm_label = tk.Label(self, text="Arm Coordinates ")
        self.arm_label.place(x=750, y=300)


        self.x_label = tk.Label(self, text="X: ")
        self.x_label.place(x=720, y=400)

        self.y_label = tk.Label(self, text="Y: ")
        self.y_label.place(x=800, y=400)

        self.z_label = tk.Label(self, text="Z: ")
        self.z_label.place(x=880, y=400)

        self.a_label = tk.Label(self, text="A: ")
        self.a_label.place(x=720, y=500)

        self.b_label = tk.Label(self, text="B: ")
        self.b_label.place(x=800, y=500)

        self.c_label = tk.Label(self, text="C: ")
        self.c_label.place(x=880, y=500)
    
    def free_lock(self):
        self.lock = False
    
    def update_label(self, label, text):
        label.config(text=text)

    def video_stream(self, cap, model_d, model_c):
    
        _, frame = cap.read()

        processed_frame, is_detected, x_pixel, y_pixel, w_pixel, h_pixel = process_frame(frame, model_d)

        if is_detected and not self.lock:
            
            self.lock = True

            self.update_label(self.object_x_label, "X :" + str(x_pixel))
            self.update_label(self.object_y_label, "Y :" + str(y_pixel))
            self.update_label(self.object_height_label, "Height :" + str(h_pixel))
            self.update_label(self.object_width_label, "Width :" + str(w_pixel))


            x_mm, y_mm, w_mm, h_mm = pixels2mm(x_pixel, y_pixel, w_pixel, h_pixel)
            
            signal_object(x_mm, y_mm)

            self.after(10000, classify_object, model_d, model_c, cap)
            self.after(10500, signal_grip, w_pixel, h_pixel)
            self.after(11000, self.free_lock)

        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(processed_frame)

        img_pil_resized = img_pil.resize((600, 400), Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(image=img_pil_resized)

        self.label_img.img_tk = img_tk
        self.label_img.configure(image=img_tk)

        self.label_img.after(20, self.video_stream, cap, model_d, model_c)
