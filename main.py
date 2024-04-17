import torch
import imageio.v2 as iio
from resnet.classifier import classify_waste
from torchvision import transforms

model = torch.load("resnet/model/trash.pth")
model.eval()

image = iio.imread("test.jpg")

transform = transforms.Compose([
      transforms.ToPILImage(),
      transforms.Resize([224,224]),
      transforms.ToTensor()
])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


print(classify_waste(model, transform(image).to(device)))



