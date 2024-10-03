import torch
from vision.detect import process_frame
from kuka.comms import move2bin

def crop_bg(frame, x, y, h, w):
    pass

def classify_object(model_d, model_c, cap, client_socket, w_up):

    _, frame = cap.read()

    _, _, x, y, h, w_down = process_frame(frame, model_d)

    cropped_frame = crop_bg(frame, x, y, h, w_down)

    # logits = model_c(cropped_frame)

    # bin = torch.argmax(logits, dim=1).cpu().detach().numpy()

    # move2bin(bin, w_up, client_socket)