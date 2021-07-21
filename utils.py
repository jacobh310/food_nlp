import requests

def get_prediction(url, review):
    data = {"input": review}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=data)

    return resp.json()

def get_predictions(url, file):

    resp = requests.post(url, files={'file' : open(file, 'rb')})
    return resp.json()