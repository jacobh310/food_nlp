import requests

def get_predict(url, review):
    """
    Sends single review to flask server and returns with a prediction
    """
    data = {"input": review}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=data)

    return resp.json()

def get_predictions(url, json):

    """
    Sends multiple reviews from a in json format to flask server
    Returns a json with reviews an predictions
    """
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=json)

    return resp.json()