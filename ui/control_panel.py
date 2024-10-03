from detection.process_video import update_frame
import tkinter as tk
from PIL import Image, ImageTk

class ControlPanel(tk.Tk):

    def __init__(self, model, title="Waste Sorter"):
        super().__init__()
        
        self.model = model

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
