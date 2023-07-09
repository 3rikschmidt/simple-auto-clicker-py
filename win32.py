import ctypes
from ctypes import *
import ctypes.wintypes as win
import datetime

ULONG_PTR = c_ulong if sizeof(c_void_p) == 4 else c_ulonglong


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", win.LONG),
        ("dy", win.LONG),
        ("mouseData", win.DWORD),
        ("dwFlags", win.DWORD),
        ("time", win.DWORD),
        ("mouseData", ULONG_PTR),
    ]


MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
# we can get away with just defining MOUSEINPUT here, as it is the largest member of the union.
# https://stackoverflow.com/a/62205935
class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_long),
        ("mi", MOUSEINPUT)
    ]


INPUT_MOUSE = 0

# https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VK_RMENU = 0xA5
VK_RIGHT_ALT = VK_RMENU
KEY_Q = ord('Q')
VK_ADD = 0x6B
VK_SUBTRACT = 0x6D
VK_OEM_COMMA = 0xBC
VK_OEM_PERIOD = 0xBE


def send_click():
    print(f'{datetime.datetime.now().isoformat()} sending click')

    # mouse down
    mouse_event = INPUT()
    mouse_event.type = INPUT_MOUSE
    mouse_event.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, 0)
    ctypes.windll.user32.SendInput(1, byref(mouse_event), sizeof(INPUT))

    # mouse up
    mouse_event.mi.dwFlags = MOUSEEVENTF_LEFTUP
    ctypes.windll.user32.SendInput(1, byref(mouse_event), sizeof(INPUT))


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getkeystate#return-value
key_states = dict()
KEY_UP = 0x8000


def has_key_been_pressed(key):
    previous_state = key_states[key] if key in key_states else 0
    state = ctypes.windll.user32.GetAsyncKeyState(key)

    has_been_pressed = False

    # Only report the key being pressed once, when
    # the state changes.
    if previous_state != state:
        key_states[key] = state

        # Two KEY_UP states are sent:
        # one with and one without the least significant bit set.
        # We'll ignore the one with it set.
        has_been_pressed = state == KEY_UP

    return has_been_pressed
