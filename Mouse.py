import win32api, win32con
import time


def mousePos(pos=(0, 0)):
    win32api.SetCursorPos(pos)


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    # print("left Click.")
    time.sleep(.015)


def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
    # print("right Click.")
    time.sleep(.015)
