#! /usr/local/bin/python3
import requests, json

class caption(object):

    def __init__(self, ocp_key):
        self.headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': ocp_key,
        }
        self.data = {
            'maxCandidates': '1',
        }
        self.api_url = "https://api.projectoxford.ai/vision/v1.0/describe"


    def describe(self, img):

        body = json.dumps({'url':img})

        try:
            r = requests.post(
                self.api_url,
                params=self.data,
                headers=self.headers,
                data=body)
            response = json.loads(r.text)
            text = response['description']['captions'][0]['text']
            return text

        except Exception as e:
            print(e)
            return None
