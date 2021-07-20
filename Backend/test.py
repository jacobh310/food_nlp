import requests
import pprint

sentence = 'If you love Mexican food, a casual ambiance, and great service...This is the place to visit.  Location-in the heart of downtown San Diego...This is my 5th or 6th time I have had lunch at La Puerta. I will continue to visit because I really am...More'
data = {"input":sentence}
url = "http://127.0.0.1:5000/predict"
url2 = "http://127.0.0.1:5000/predictions"
headers = {"Content-Type": "application/json"}

resp = requests.post(url, headers=headers, json=data)
resp2 = requests.post(url2, files={'file' : open("Los Angeles_restaurant only reviews.csv", 'rb')})

# print(resp.json())
pprint.pprint(resp2.json())

# import utils
# import pandas as pd
# import tensorflow as tf
# import numpy as np
# import pprint
# df = pd.read_csv("Los Angeles_restaurant only reviews.csv")
# pickle_path = "tv_layer.pkl"
# model_path = 'lstm_finetune_novec.h5'
#
# import json
# model, vectorizer = utils.load_model_vectorizer(model_path, pickle_path)
#
# def predict_csv(df):
#     x = df.values
#     x_vec = vectorizer(x)
#     probs = model.predict(x_vec)
#     preds = tf.cast(tf.round(probs), tf.int32)
#     preds = tf.squeeze(preds).numpy().tolist()
#     pred_data = pd.DataFrame.from_dict({'review': np.squeeze(x, axis=-1),
#                                         'predictions': preds}, )
#
#     return pred_data.to_json(orient='records')
#
# pprint.pprint(predict_csv(df))