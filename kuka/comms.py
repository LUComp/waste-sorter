from typing import Callable, Optional
from events.event import EventLoop
from kuka.constants import HOME_POS, TOOL_ANGLE
from utils import width2angle
from kuka_comm_lib import KukaRobot


def signal_grip(angle, client_socket):
    if angle == 0:
        angle = 90
    client_socket.send(angle)

def queuemove(e: EventLoop, r: KukaRobot, func: Callable):
    e.run_and_wait(func, r.is_ready_to_move)
    
def queuegrip(e: EventLoop, angle, client_socket):
    e.run(lambda: signal_grip(angle, client_socket))
    e.sleep(2000)
    
def movehome(r: KukaRobot):
    r.goto(HOME_POS[0], HOME_POS[1], HOME_POS[2], TOOL_ANGLE[0], TOOL_ANGLE[1], TOOL_ANGLE[2])