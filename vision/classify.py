from typing import Callable
from cv2 import VideoCapture
import cv2
from kuka_comm_lib import KukaRobot
import torch
from events.event import EventLoop
from kuka.constants import BIN_DICT, CLASSIFY_HEIGHT, OBJECT_HEIGHT
from kuka.comms import movehome, queuegrip, queuemove
import numpy as np
from torchvision import transforms
import tkinter as tk

def classify_object(
    model_c,
    cap: VideoCapture,
    rp_socket,
    grip_angle: float,
    eloop: EventLoop,
    robot: KukaRobot,
    unlock: Callable,
    class_label: tk.Label
):
    _, frame = cap.read()
    
    img = process_image(frame)
    logits = model_c(img)
    dest_bin = int(torch.argmax(logits, dim=1).item())

    class_label.config(text=f"Object Type: {get_label(dest_bin)}")
    # move to object
    queuegrip(eloop, 90, rp_socket)
    # move into position around/above object
    queuemove(eloop, robot, lambda: robot.goto(z=OBJECT_HEIGHT))
    # close around object
    queuegrip(eloop, 0, rp_socket)
    # queuegrip(eloop, grip_angle, rp_socket)
    # move up
    queuemove(eloop, robot, lambda: robot.goto(z=CLASSIFY_HEIGHT))

    bin_x, bin_y = BIN_DICT[dest_bin]

    queuemove(eloop, robot, lambda: robot.goto(bin_x, bin_y))
    queuemove(eloop, robot, lambda: robot.goto(z=OBJECT_HEIGHT))
    queuegrip(eloop, 90, rp_socket)
    queuemove(eloop, robot, lambda: robot.goto(z=CLASSIFY_HEIGHT))
    queuegrip(eloop, 0, rp_socket)

    queuemove(eloop, robot, lambda: movehome(robot))
    eloop.run(unlock)

def process_image(img):
    transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize([224,224]),
    transforms.ToTensor()
    ])

    device = torch.device("cuda")

    return transform(img).unsqueeze(0).to(device)

def get_label(idx):
    labels = ["metal", "misc", "plastic", "glass", "paper", "cardboard"]
    return(labels[idx])