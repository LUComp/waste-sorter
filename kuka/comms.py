from utils import width2angle
from kuka_comm_lib import KukaRobot

def move2coords(x, y, robot: KukaRobot, home=False):
    if home:
        robot.home()
    robot.goto(x, y)

def move2bin(bin, w, client_socket):

    signal_grip(w, client_socket)

def signal_grip(w, client_socket):
    if w == 0:
        angle = 90
    else:
        angle =  width2angle(w)
    client_socket.send(angle)
