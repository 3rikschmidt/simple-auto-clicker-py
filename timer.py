import threading
from typing import Callable, Optional


class Timer:
    interval_ms: int
    fn: Callable
    is_running: bool = False
    timer: Optional[threading.Timer] = None

    def __init__(self, interval_ms: int, fn: Callable):
        if interval_ms <= 0:
            raise "interval needs to be > 0"

        self.interval_ms = interval_ms
        self.fn = fn

    def start(self):
        def tick():
            if self.is_running:
                self.fn()
                self.start()

        self.is_running = True
        self.timer = threading.Timer(self.interval_ms / 1000.0, tick)
        self.timer.start()

    def stop(self):
        self.is_running = False
        if self.timer is not None:
            self.timer.cancel()

    def toggle(self):
        if self.is_running:
            print('stop')
            self.stop()
        else:
            print('start')
            self.start()

    def increase_interval(self, delta_ms):
        new_interval = self.interval_ms + delta_ms
        if new_interval > 0:
            self.interval_ms = new_interval
            print(f'New interval: {self.interval_ms}ms')
