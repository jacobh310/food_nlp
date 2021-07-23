import os
import json



class Config:
    BUCKET_NAME = 'food-nlp-data'
    PROJECT_NAME = 'calm-spring-320419'

class DevConfig(Config):
    URL_PREDICTIONS = "http://127.0.0.1:5000/predictions"
    URL_PREDICT = "http://127.0.0.1:5000/predict"
    GOOGLE_APPLICATION_CREDENTIALS = "calm-spring-320419-39eded0b835c.json"

# class ProdConfig(Config):
#     URL_PREDICTIONS = os.environ.get("URL_PREDICTIONS")
#     URL_PREDICT = os.environ.get("URL_PREDICT")
#     GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

