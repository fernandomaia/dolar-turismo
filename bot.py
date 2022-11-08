import json
import requests
import time
import melhorcambio
import os

URL = "https://api.telegram.org/bot{}/".format(os.environ['DOLAR_TURISMO_TOKEN'])

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf-8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id, reply_markup=None):
    if text == "/start":
        text = """ Olá!
        Este bot irá te ajudar a obter a cotação mais atualizada do dólar turismo.
        Para isso, basta enviar uma mensagem escrito Cotação e eu te retornarei essa informação.
        Por favor, entenda que este bot está em uma versão experimental, então existem muitas melhorias a serem feitas.

        Espero que você aproveite!

        @fmaia"""
    elif text == "Cotação":
        text = melhorcambio.main()
    else:
        text = ""
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            keyboard = build_keyboard()
            send_message(text, chat, keyboard)
        except Exception as e:
            print(e)

def build_keyboard():
    keyboard = [["Cotação"]]
    reply_markup = {"keyboard": keyboard}
    return json.dumps(reply_markup)

def main():
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            print("Update:" + str(updates))
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        else:
            print('MainError:' + str(updates))
        time.sleep(0.5)

if __name__ == '__main__':
    main()
