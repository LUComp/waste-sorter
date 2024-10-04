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

        self.configure(bg="#2596be")
  
        self.create_video_frame()
        self.create_labels()

        self.lock = False
    
    def create_video_frame(self):
        self.frame_video = tk.Frame(self, width=600, height=400, bg="#2596be")
        self.frame_video.grid(row=0, column=0, padx=10, pady=10)

        self.label_img = tk.Label(self.frame_video, width=600, height=400, bg="#2596be")
        self.label_img.grid(row=0, column=0, padx=10, pady=10)

    def create_labels(self):
        self.object_label = tk.Label(self, text="Object Details", bg="white", fg="black", font=("Arial", 25))
        self.object_label.place(x=750, y=50)

        self.object_detected_label = tk.Label(self, text="Object Detected : False", bg="#f08c64", fg="white", font=("Ubuntu", 20))
        self.object_detected_label.place(x=720, y=150)

        self.object_x_label = tk.Label(self, text="X : ", bg="#f08c64", fg="white", font=("Ubuntu", 18))
        self.object_x_label.place(x=700, y=200)

        self.object_y_label = tk.Label(self, text="Y : ", bg="#f08c64", fg="white", font=("Ubuntu", 18))
        self.object_y_label.place(x=850, y=200)

        self.object_height_label = tk.Label(self, text="Height : ", bg="#f08c64", fg="white", font=("Ubuntu", 18))
        self.object_height_label.place(x=700, y=250)

        self.object_width_label = tk.Label(self, text="Width : ", bg="#f08c64", fg="white", font=("Ubuntu", 18))
        self.object_width_label.place(x=850, y=250)


        self.arm_label = tk.Label(self, text="Arm Coordinates ", bg="white", fg="black", font=("Arial", 25))
        self.arm_label.place(x=720, y=350)


        self.x_label = tk.Label(self, text="X: ", bg="#f08c64", fg="white", font=("Ubuntu", 18))
        self.x_label.place(x=720, y=450)

        self.y_label = tk.Label(self, text="Y: ", bg="#f08c64", fg="white", font=("Ubuntu", 18))
        self.y_label.place(x=800, y=450)

        self.z_label = tk.Label(self, text="Z: ", bg="#f08c64", fg="white", font=("Ubuntu", 18))
        self.z_label.place(x=880, y=450)

        self.a_label = tk.Label(self, text="A: ", bg="#f08c64", fg="white", font=("Ubuntu", 18))
        self.a_label.place(x=720, y=550)

        self.b_label = tk.Label(self, text="B: ", bg="#f08c64", fg="white", font=("Ubuntu", 18))
        self.b_label.place(x=800, y=550)

        self.c_label = tk.Label(self, text="C: ", bg="#f08c64", fg="white", font=("Ubuntu", 18))
        self.c_label.place(x=880, y=550)
    
    def free_lock(self):
        self.lock = False
    
    def update_label(self, label, text):
        label.config(text=text)

    def video_stream(self, cap, model_d, model_c):
    
        _, frame = cap.read()

        processed_frame, is_detected, x_pixel, y_pixel, w_pixel, h_pixel = process_frame(frame, model_d)

        self.update_label(self.object_detected_label, "Object Detected : " + str(is_detected))


        if is_detected and not self.lock:
            
            self.lock = True

            self.update_label(self.object_x_label, "X : " + str(x_pixel))
            self.update_label(self.object_y_label, "Y : " + str(y_pixel))
            self.update_label(self.object_height_label, "Height : " + str(h_pixel))
            self.update_label(self.object_width_label, "Width : " + str(w_pixel))

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
