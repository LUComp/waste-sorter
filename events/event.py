from enum import Enum
from queue import Queue, Empty as QueueEmpty
from typing import Any, Callable, Literal, NamedTuple, Union


class EventType(Enum):
    SLEEP = 1
    FUNC = 2
    SLEEP_UNTIL = 3


class Event(NamedTuple):
    type: EventType
    data: dict


class EventLoop:
    event_queue: Queue[Event]
    after: Callable[[Union[int, Literal["idle"]], Callable], Any]

    def __init__(self, trigger_func: Callable[[Union[int, Literal["idle"]], Callable], Any]):
        self.event_queue = Queue()
        self.after = trigger_func

    def start(self):
        self.handle_event()

    def handle_event(self):
        try:
            event = self.event_queue.get_nowait()
        except QueueEmpty:
            # no events, wait.
            self.after(100, self.handle_event)
            return

        if event.type == EventType.SLEEP:
            self.after(event.data["duration"], self.handle_event)
        elif event.type == EventType.FUNC:
            event.data["func"]()
            self.after(100, self.handle_event)
        elif event.type == EventType.SLEEP_UNTIL:
            self._sleep_until(event.data["func"])
        else:
            self.after(100, self.handle_event)
            raise ValueError("Unimplemented event type: " + str(event.type))

    def run(self, func: Callable):
        self.event_queue.put_nowait(Event(EventType.FUNC, {"func": func}))

    def sleep(self, duration):
        self.event_queue.put_nowait(Event(EventType.SLEEP, {"duration": duration}))

    def sleep_until(self, func: Callable[[], bool]):
        self.event_queue.put_nowait(Event(EventType.SLEEP_UNTIL, {"func": func}))

    def run_and_wait(self, func: Callable, condition: Callable[[], bool]):
        self.run(func)
        self.sleep_until(condition)

    def _sleep_until(self, func: Callable[[], bool]):
        result = func()
        if result:
            self.after(100, self.handle_event)
        else:
            self.after(100, lambda: self._sleep_until(func))
