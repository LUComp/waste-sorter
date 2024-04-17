import torch

def classify_waste(model, img, str=False):
    with torch.no_grad():
        logits = model(img)
        out = torch.argmax(logits, dim=1)
        if str:
            return get_label(out)
        else:
            return out.item()
            
def get_label(x):
    labels = ["paper", "cardboard", "metal", "trash", "plastic", "glass"]
    return(labels[x])