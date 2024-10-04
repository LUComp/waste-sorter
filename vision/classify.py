from typing import Callable
from cv2 import VideoCapture
import cv2
from kuka_comm_lib import KukaRobot
import torch
from events.event import EventLoop
from kuka.constants import BIN_DICT, CLASSIFY_HEIGHT, OBJECT_HEIGHT
from kuka.comms import movehome, queuegrip, queuemove
import numpy as np

def classify_object(
    model_c,
    cap: VideoCapture,
    client_socket,
    grip_angle: float,
    eloop: EventLoop,
    robot: KukaRobot,
    unlock: Callable,
):
    _, frame = cap.read()
    frame = cv2.resize(frame, (224, 224))
    frame = np.transpose(frame, (2, 0, 1))
    frame = torch.tensor(frame, dtype=torch.float).to("cuda")
    frame = frame.unsqueeze(0)

    # _, _, x, y, h, w_down = process_frame(frame, model_d)
    # cropped_frame = crop_bg(frame, x, y, h, w_down)
    cropped_frame = frame
    logits = model_c(cropped_frame)

    dest_bin = int(torch.argmax(logits, dim=1).item())

    # move2bin(bin, w_up, client_socket)

    # move to object
    queuegrip(eloop, 0, client_socket)
    # move into position around/above object
    queuemove(eloop, robot, lambda: robot.goto(z=OBJECT_HEIGHT))
    # close around object
    queuegrip(eloop, grip_angle, client_socket)
    # move up
    queuemove(eloop, robot, lambda: robot.goto(z=CLASSIFY_HEIGHT))

    bin_x, bin_y = BIN_DICT[dest_bin]

    queuemove(eloop, robot, lambda: robot.goto(bin_x, bin_y))
    queuemove(eloop, robot, lambda: robot.goto(z=OBJECT_HEIGHT))
    queuegrip(eloop, 0, client_socket)
    queuemove(eloop, robot, lambda: robot.goto(z=CLASSIFY_HEIGHT))
    # make the gripper appear closed when not in use
    queuegrip(eloop, 1, client_socket)

    queuemove(eloop, robot, lambda: movehome(robot))
    eloop.run(unlock)
