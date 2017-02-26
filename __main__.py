#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
import requests, json, time, urllib
import gottago, imageCaption
import configparser
import random

config = configparser.RawConfigParser()
config.read('config.ini')

responses_insults = config.get('Responses','insults')
TOKEN = config.get('General','telegram_token')

URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def getURL(url):
    response = requests.get(url)
    content = response.content.decode("utf-8")
    return content

def get_last_update_id(updates):
    update_ids = [ y['update_id'] for y in updates]
    return max(update_ids)

def get_file_path(file_id):
    url = URL + "getFile?file_id={}".format(file_id)
    data = json.loads(getURL(url))
    return data['result']['file_path']

def get_file(file_path):
    URL = "https://api.telegram.org/file/bot{}/".format(TOKEN)
    url = URL + file_path
    return url


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url = url + "?offset={}".format(offset)
    data = getURL(url)
    dataJSON = json.loads(data)
    d = dataJSON['result']
    return d

def send_response(chat, text):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat)
    getURL(url)

def send_location(chat, coords):
    url = URL + "sendLocation?chat_id={}&latitude={}&longitude={}".format(
        chat,
        coords[0],
        coords[1]
    )
    getURL(url)

def echo_all(updates):
    for item in updates:
        try:
            chat = item['message']['chat']['id']
            try:
                text = item['message']['text']
                msg = 'text'
            except:
                print("text not found.")
                pass
            try:
                text = item['message']['photo']
                print(text)
                text = text[len(text)-1]['file_id']
                print(text)
                msg = 'photo'
            except:
                print('photo not found')
                pass
            print(msg + " : " + text)
            try:
                text = text.replace('@kotek_bot','')
            except:
                print('@kotek_bot removed from msg.')
        except:
            chat = ""
            text = ""
            msg = None
        print("{}: {}".format(chat, text))

        if msg == 'text':
            if text[:3] == "/wc":
                data = gottago.find(text[3:])
                if data:
                    text = data[0]
                    coords = data[1]
                    send_location(chat, coords)
            elif text[:3] == "/fu":
                text = fuck_off()
            elif text[:3] == "/ha":
                text = joke()
            elif text[:1] == "/":
                text = what()
            else:
                text = ""
        elif msg == 'photo':
            file_path = get_file_path(text)
            file_url = get_file(file_path)
            print(file_url)
            text = imageCaption.description(file_url)

        send_response(chat, "{}".format(text))

def fuck_off():
    with open('foff.txt', 'r') as f:
        insults = [ line.strip() for line in f]
    rnd = random.randint(0,len(insults)-1)
    return insults[rnd]

def joke():
    with open('jokes.txt', 'r') as f:
        jokes = [ line.strip() for line in f]
    rnd = random.randint(0,len(jokes)-1)
    return jokes[rnd]

def what():
    with open('what.txt', 'r') as f:
        what = [ line.strip() for line in f]
    rnd = random.randint(0,len(what)-1)
    return what[rnd]

def image():
    return None

def main():
    last_update_id = None
    fuck_off()
    while True:
        updates = get_updates(last_update_id)
        if len(updates) > 0:
            last_update_id = get_last_update_id(updates)+1
            echo_all(updates)
    time.sleep(2)

if __name__ == '__main__':
    main()
