import seriallib.armcontroller
import torch
from resnet.classifier import classify_waste
from detection.detection import get_waste_image
import seriallib

model = torch.load("resnet/model/trash.pth")
model.eval()

armcontroller = seriallib.ArmController("mock") # dont connect to arm over serial, just say it is successful instantly
## ensure arduino ide/anything else using the serial port is closed.
# armcontroller = seriallib.ArmController("/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_8513332303635140E1A0-if00") # this is correct for the standard arduino on linux
# armcontroller = seriallib.ArmController("COM3") # windows, change to match serial port shown in arduino ide?

bin1_labels = ["metal", "glass"]
bin2_labels = ["paper", "cardboard"]
bin3_labels = ["trash", "plastic"]


def main():
      while True:
            # detect if there is an object
            img = get_waste_image(0)

            # img present, pickup with arm.
            armcontroller.grab()
            
            # process the image and classify it
            label = classify_waste(model, img, output_as_string=True)
            
            if label in bin1_labels:
                  armcontroller.move_bin1()
            elif label in bin2_labels:
                  armcontroller.move_bin2()
            else:
                  # fallback to bin 3
                  armcontroller.move_bin3()
                           
            print(label)

main()
