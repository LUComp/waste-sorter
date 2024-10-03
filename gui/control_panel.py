import tkinter as tk
from PIL import Image, ImageTk
import cv2
from vision.detect import process_frame
from vision.classify import classify_object
from utils.comms import signal_grip

class ControlPanel(tk.Tk):

    def __init__(self, title="Waste Sorter"):
        super().__init__()

        self.title("Waste Sorter")        #set title of main window
        self.geometry("1000x600")                #set size of main window
  
        self.create_video_frame()
        self.create_labels()
    
    def create_video_frame(self):
        self.frame_video = tk.Frame(self, width=600, height=400)
        self.frame_video.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.label_img = tk.Label(self.frame_video, width=600, height=400)
        self.label_img.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    def create_labels(self):
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

        self.height_label = tk.Label(self, text="Height: ")
        self.height_label.grid(row=2, column=1, padx=10, pady=10)
    
    def video_stream(self, cap, model_d, model_c):
    
        _, frame = cap.read()

        processed_frame, is_mid,_,_,w,h = process_frame(frame, model_d)

        if is_mid:
            print("Object detected, waiting 2 seconds...")
            self.after(2000, classify_object, model_d, model_c)
            self.after(2500, signal_grip, w, h)

        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(processed_frame)

        img_pil_resized = img_pil.resize((600, 400), Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(image=img_pil_resized)

        self.label_img.img_tk = img_tk
        self.label_img.configure(image=img_tk)

        self.label_img.after(10, self.video_stream, cap, model_d, model_c)
