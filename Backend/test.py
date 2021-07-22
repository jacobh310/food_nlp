import requests
import pprint

review= 'If you love Mexican food, a casual ambiance, and great service...This is the place to visit.  Location-in the heart of downtown San Diego...This is my 5th or 6th time I have had lunch at La Puerta. I will continue to visit because I really am...More'
data = {"input":review}


url = "http://127.0.0.1:5000/predict"
url2 = "http://127.0.0.1:5000/predictions"
headers = {"Content-Type": "application/json"}

resp = requests.post(url, headers=headers, json=data)
# resp2 = requests.post(url2, files={'file' : open("Los Angeles_restaurant only reviews.csv", 'rb')})
resp2 = requests.post(url2, headers=headers, )

print(resp.json())
pprint.pprint(resp2.json())

# import os
# from google.cloud import storage
#
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../calm-spring-320419-39eded0b835c.json"
#
# blob_name = "Los Angeles_restaurant only reviews.csv"
# file_path= r'C:\Users\jacob\Desktop\Fast Food REviews'
# bucket_name = 'food-nlp-data'
#
# def upload_to_bucket(blob_name, file_path, bucket_name):
#     client = storage.Client()
#     bucket = client.get_bucket(bucket_name)
#     blob = bucket.blob(blob_name)
#     blob.upload_from_filename(file_path)
#
#
# upload_to_bucket(blob_name, os.path.join(file_path, blob_name), bucket_name)