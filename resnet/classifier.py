import torch
import numpy as np
from torchvision import transforms

def classify_waste(model, img, output_as_string=False):

    img = process_image(img)

    with torch.no_grad():
        logits = model(img)
        out = torch.argmax(logits, dim=1)
        if output_as_string:
            print(np.round(torch.nn.Softmax(1)(logits).cpu().numpy()  , 3))
            return get_label(out)
        else:
            return out.item()

def get_label(x):
    labels = ["metal", "trash", "plastic", "glass", "paper", "cardboard"]
    return(labels[x])

def process_image(img):
    transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize([224,224]),
    transforms.ToTensor()
    ])

    device = torch.device("cuda")

    return transform(img).unsqueeze(0).to(device)
