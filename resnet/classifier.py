import torch

def classify_waste(model, img):
    with torch.no_grad():
        logits = model(img)
        out = torch.argmax(logits, dim=1)
        return get_label(out)

def get_label(x):
    labels = ["paper", "cardboard", "metal", "trash", "plastic", "glass"]
    return(labels[x])