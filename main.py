import signal

from timer import Timer
from win32 import send_click, has_key_been_pressed, VK_RIGHT_ALT, KEY_Q, VK_OEM_COMMA, VK_OEM_PERIOD

name = "Erik's Auto-Clicker v0.1"


def main():
    print(name)

    stopped = False
    timer = Timer(1500, send_click)

    def end_loop():
        nonlocal stopped
        stopped = True
        timer.stop()

    # handle ctrl+c
    signal.signal(signal.SIGINT, lambda sig, frame: end_loop())

    while not stopped:
        if has_key_been_pressed(KEY_Q):
            end_loop()
        if has_key_been_pressed(VK_RIGHT_ALT):
            timer.toggle()
        if has_key_been_pressed(VK_OEM_PERIOD):
            timer.increase_interval(100)
        if has_key_been_pressed(VK_OEM_COMMA):
            timer.increase_interval(-100)


if __name__ == '__main__':
    main()
