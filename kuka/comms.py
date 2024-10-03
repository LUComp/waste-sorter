from typing import Callable, Optional
from events.event import EventLoop
from utils import width2angle
from kuka_comm_lib import KukaRobot

def move2coords(x, y, robot: KukaRobot, home=False):
    if home:
        robot.home()
    robot.goto(x, y)

def move2bin(event_loop: EventLoop, bin, robot: KukaRobot, w, client_socket):
    event_loop.run(lambda: robot.goto(0, 0))
    event_loop.sleep(500)
    event_loop.run(lambda: signal_grip(w, client_socket))

def signal_grip(w, client_socket):
    if w == 0:
        angle = 90
    else:
        angle =  width2angle(w)
    client_socket.send(angle)

def queuemove(e: EventLoop, r: KukaRobot, func: Callable):
    e.run_and_wait(func, r.is_ready_to_move)
    
def queuegrip(e: EventLoop, angle, client_socket):
    e.run(lambda: signal_grip(angle, client_socket))
    e.sleep(2000)