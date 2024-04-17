import torch
import imageio as iio
from resnet.classifier import classify_waste

model = torch.load("resnet/model/trash.pth")
model.eval()

print(classify_waste(iio.imread(model, "test.jpg")))



