from detection.process_video import update_frame
from ui.control_panel import ControlPanel
import cv2
import torch

if __name__ == "__main__":      

      model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
      cap = cv2.VideoCapture(0)

      panel = ControlPanel(model, "Waste Sorter")

      update_frame(cap, panel)

      panel.mainloop()

      # Release the webcam when the window is closed
      cap.release()
      cv2.destroyAllWindows()


