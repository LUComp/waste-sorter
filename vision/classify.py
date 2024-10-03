import torch
from vision.detect import process_frame
from kuka.comms import send_bin

def crop_bg(frame, x, y, h, w):
    pass

def classify_object(model_d, model_c, cap):

    _, frame = cap.read()

    _, _, x, y, h, w = process_frame(frame, model_d)

    cropped_frame = crop_bg(frame, x, y, h, w)

    # logits = model_c(cropped_frame)

    # bin = torch.argmax(logits, dim=1).cpu().detach().numpy()

    # send_bin(bin)