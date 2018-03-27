# basic telegram bot
# https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay
# https://github.com/sixhobbits/python-telegram-tutorial/blob/master/part1/echobot.py

import json
import requests
import time
import sys
import urllib
import config
from syllable import generate_haiku, format_haiku
from syllable import clappify
#python3: urllib.parse.quote_plus
# python2: urllib.pathname2url

URL = "https://api.telegram.org/bot{}/".format(config.TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
    greetings = ['hi bot', 'hello bot', 'good day bot', 'sup bot', 'whats up', 'hey', 'good moring bot', 'greetings bot']
    goodbye = ['bye bot', 'bye bye bot', 'goodbye bot', 'see you bot', 'see you later bot', 'c u bot', 'adieu bot']
    instructions = ['info', 'instructions', 'help', 'information', 'what', 'commands']
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            if text[0] == "👏":
                send_message(clappify(text[1:]), chat)
            elif any(text.lower() in s for s in instructions):
                send_message(format_haiku("Write something like hi, info or adieu to get scripted responses."), chat)
                send_message(format_haiku("Put a clap(👏) at the start of your message and I will clap it for you"), chat)
                send_message(format_haiku("Lastly, give me text and I will try to format it as a haiku."), chat)
            elif len(text.split()) > 5:
                send_message(generate_haiku(text), chat)
            elif any(text.lower() in s for s in greetings):
                send_message(format_haiku("Hello there friend, nice to see you again. How can I be of service?"), chat)
            elif any(text.lower() in s for s in goodbye):
                send_message(format_haiku("Sad to see you go, but all the nice meetings have to come to an end."), chat)
            elif text == "🤖🔫":
                send_message(format_haiku("Be careful with that artillery what do you think you are doing?!"), chat)
            else:
                send_message(format_haiku("Your message was not something I could spot as a command or haiku"), chat)
                send_message(format_haiku("Please do try to send 'info' to prompt a list of commands that I know"), chat)
        except KeyError:
            pass


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text) # urllib.parse.quote_plus(text) # (python3)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.1)


if __name__ == '__main__':
    main()
