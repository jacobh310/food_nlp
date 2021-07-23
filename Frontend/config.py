import os


class DevConfig():
    URL_PREDICT = "https://food-nlp-g5yr3ihzpq-uw.a.run.app/predict"
    URL_PREDICTIONS = "https://food-nlp-g5yr3ihzpq-uw.a.run.app/predictions"
    BUCKET_NAME = 'food-nlp-data'
    PROJECT_NAME = 'calm-spring-320419'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "calm-spring-320419-39eded0b835c.json"



class ProdConfig():
    URL_PREDICT  =  os.environ.get('URL_PREDICT')
    URL_PREDICTIONS = os.environ.get('URL_PREDICTIONS')
    PROJECT_NAME = os.environ.get('PROJECT_NAME')
    BUCKET_NAME = os.environ.get('BUCKET_NAME')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"
