import seriallib.armcontroller
import seriallib.exceptions
import seriallib.armcontroller
import seriallib.exceptions
import torch
from resnet.classifier import classify_waste
from detection.detection import detect_movement, detect_object
import seriallib
import time
import cv2
import imageio as iio

model = torch.load("resnet/model/trash.pth")
model.eval()

# armcontroller = seriallib.ArmController("mock") # dont connect to arm over serial, just say it is successful instantly
## ensure arduino ide/anything else using the serial port is closed.
armcontroller = seriallib.ArmController("/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_8513332303635140E1A0-if00") # this is correct for the standard arduino on linux
# armcontroller = seriallib.ArmController("COM3") # windows, change to match serial port shown in arduino ide?

bin1_labels = ["metal", "glass", "misc"]
bin2_labels = ["paper", "cardboard", "metal"]

def camera_preview():
      starttime = time.time()
      frame = None

      while time.time() - starttime < 0.1:
            cap = cv2.VideoCapture(0)  # Try different API here
            ret, frame = cap.read()
            if not ret:
                  print("Error: Failed to capture frame")
                  break
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                  break

      cap.release()
      cv2.imwrite('c2.jpg',frame)


def main():
      print("started")
      cap = cv2.VideoCapture(0) 
      ret, frame = cap.read()
      # print("RET", ret)
      print("img taken")
      cv2.imwrite('c1.jpg',frame)
      cap.release()
      img = ""

      while True:
            camera_preview()
            if detect_movement():
                  img = detect_object()
                  if img != "":
                        break
      
      # process the image and classify it
      label = classify_waste(model, iio.imread(img), output_as_string=True)

      try:
            # img present, pickup with arm.
            armcontroller.grab()
      except seriallib.exceptions.ArmException as e:
            print(e)
      
      try:
            if label in bin1_labels:
                  armcontroller.move_bin1()
            elif label in bin2_labels:
                  armcontroller.move_bin2()
      
      except seriallib.exceptions.ArmException as e:
            print(e)
      
      print(label)

      cv2.destroyAllWindows()
                        

main()
