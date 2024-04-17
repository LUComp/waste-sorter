def classify_waste(model, img):
    with torch.no_grad():
        logits = model(img)
        return torch.argmax(logits, dim=1)