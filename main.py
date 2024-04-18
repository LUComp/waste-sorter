import torch
from resnet.classifier import classify_waste
from detection.detection import get_waste_image

model = torch.load("resnet/model/trash.pth")
model.eval()

def main():
      while True:
            # detect if there is an object
            img = get_waste_image()

            # process the image and classify it
            label = classify_waste(model, img, str=True)
            
            print(label)

main()