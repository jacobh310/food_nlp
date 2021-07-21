import requests
import pprint

review= 'If you love Mexican food, a casual ambiance, and great service...This is the place to visit.  Location-in the heart of downtown San Diego...This is my 5th or 6th time I have had lunch at La Puerta. I will continue to visit because I really am...More'
data = {"input":review}
url = "http://127.0.0.1:5000/predict"
url2 = "http://127.0.0.1:5000/predictions"
headers = {"Content-Type": "application/json"}

resp = requests.post(url, headers=headers, json=data)
# resp2 = requests.post(url2, files={'file' : open("Los Angeles_restaurant only reviews.csv", 'rb')})

print(resp.json())
# pprint.pprint(resp2.json())




