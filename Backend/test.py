import requests
sentence = 'If you love Mexican food, a casual ambiance, and great service...This is the place to visit.  Location-in the heart of downtown San Diego...This is my 5th or 6th time I have had lunch at La Puerta. I will continue to visit because I really am...More'
data = {"input":sentence}
url = "http://127.0.0.1:5000/predict"
headers = {"Content-Type": "application/json"}

resp = requests.post(url, headers=headers, json=data)

print(resp.json())