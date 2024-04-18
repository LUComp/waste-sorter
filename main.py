# import torch
# from resnet.classifier import classify_waste
from detection.detection2 import detect_movement, detect_object
import cv2
import time

# model = torch.load("resnet/model/trash.pth")
# model.eval()


def camera_preview():
      starttime = time.time()
      frame = None

      while time.time() - starttime < 0.2:
            cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Try different API here
            ret, frame = cap.read()
            if not ret:
                  print("Error: Failed to capture frame")
                  break
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                  break

      cap.release()
      # cv2.destroyAllWindows()
      cv2.imwrite('c2.jpg',frame)


def main():
      print("started")
      cap = cv2.VideoCapture(1) 
      ret, frame = cap.read()
      # print("RET", ret)
      print("img taken")
      cv2.imwrite('c1.jpg',frame)
      cap.release()

      while True:
            camera_preview()
            if detect_movement():
                  img = detect_object()
                  if img != "":
                        break
                        

main()