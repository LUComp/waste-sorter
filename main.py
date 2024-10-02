from detection.process_video import update_frame
from ui.control_panel import ControlPanel
import cv2
import ssl
import torch

def main():

      control_panel = ControlPanel(cap, model)



      # SSL
      ssl._create_default_https_context = ssl._create_unverified_context

      # YOLOv5
      model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

      cap = cv2.VideoCapture(0)

      control_panel = ControlPanel()    #instantiate and start communication options window

      update_frame(cap, model)

      control_panel.start()

      # Release the webcam when the window is closed
      cap.release()
      cv2.destroyAllWindows()

if __name__ == "__main__":                 
      main()


