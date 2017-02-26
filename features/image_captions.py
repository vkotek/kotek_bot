#! /usr/local/bin/python3
import requests, json

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'c2e1b38b6f48412a81bdb05de3456419',
}
data = {
    'maxCandidates': '1',
}

#img = "http://stage.philosophizethis.org/wp-content/uploads/2016/10/Nietzsche-274x300-1.jpg"
api_url = "https://api.projectoxford.ai/vision/v1.0/describe"


def description(img):
    body = json.dumps({'url':img})
    try:
        r = requests.post(api_url, params=data, headers=headers, data=body)
        print(r.url)
        response = json.loads(r.text)
        print(response)
        text = response['description']['captions'][0]['text']
        return text
    except Exception as e:
        print(e)
        return None
