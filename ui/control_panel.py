from detection.process_video import update_frame
import tkinter as tk
from PIL import Image, ImageTk

class ControlPanel(tk.Tk):

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

        #self.takephoto_button = tk.Button(self, text="Take Photo", command=self.example)
        #self.takephoto_button.grid(row=1, column=0, padx=10, pady=10)
    
    #def set_x_position():


    #def set_y_position():

    def start(self):
        self.mainloop()                                #start tkinter mainloop

    def update_interface_image():
    
        img_tk = ImageTk.PhotoImage(image=img_pil_resized)

        # Update the tkinter label with the new frame
        self.label_img.config(image=img_tk)
        self.label_img.image = img_tk

if __name__ == "__main__":                 
    img_tk = update_frame()
    ControlPanel.start()

    # Update the tkinter label with the new frame
    control.config(image=img_tk)
    control_panel.label_img.image = img_tk

    # Schedule the next frame update (16 ms corresponds to ~60 FPS)
    control_panel.after(16, update_frame(cap, model, control_panel))

    # Release the webcam when the window is closed
    cap.release()
    cv2.destroyAllWindows()

