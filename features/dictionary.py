# -*- coding: utf-8 -*-
import json
import sys
from urllib import parse, request

class dictionary(object):

    legal_translations = ['en-ru', 'ru-en', 'en-en', 'ru-ru']

    # Initialize function, get config from file
    def __init__(self, api_url, api_key):
        self.cfg_url = api_url
        self.cfg_key = api_key

    def get(self, word, lang):
        url = self.cfg_url.format(self.cfg_key, lang, word)
        url = parse.quote(url, safe=':/?&=')
        try:
            with request.urlopen(url) as data:
                data = json.loads(data.read().decode('utf8'))
                data = data['def']
            return data
        except:
            e = sys.exc_info()
            error = "Error getting definition. Sorry.\n\n%s\n\n%s" % (url,e)
            return error

    def parse(self, params):
        if params[0] not in self.legal_translations:
            pass
        print(params)
        try:
            response = self.get(params[1], params[0])
            print(params)
            text = []
            item = []
            for df in response:
                item.append[df['text']]
                for word in df['tr']:
                    text.append(word['text'])
                text.append('\n')
            return ', '.join(text)
        except:
            return 'No definition found.'

if __name__ == "__main__":
    d = dictionary("config.ini")
    df = d.get("сука","ru-en")
    print(df)
