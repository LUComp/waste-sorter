import torch
import imageio.v2 as iio
from resnet.classifier import classify_waste
from torchvision import transforms

model = torch.load("resnet/model/trash.pth")
model.eval()

image = iio.imread("glass_001.jpg")

transform = transforms.Compose([
      transforms.ToPILImage(),
      transforms.Resize([224,224]),
      transforms.ToTensor()
])

device = torch.device("cuda")

image = transform(image).unsqueeze(0).to(device)

print(classify_waste(model, image))



