import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
import utils
import json
from flask import Flask, request, jsonify
import pandas as pd

pickle_path = "tv_layer.pkl"
model_path = 'lstm_finetune_novec.h5'

model, vectorizer = utils.load_model_vectorizer(model_path, pickle_path)

def predict(review):
  """
  Takes in a review and returns a prediction on whether it is a 5 star review
  """
  x_vec = vectorizer(np.array([review]))
  prob = model.predict(x_vec)[0]

  return tf.round(prob).numpy()[0]

def predict_csv(df):
  """"
  Takes in a pandas dataframe of reviews and returns a json string with reviews and predictions
  """
  x = df.values
  x_vec = vectorizer(x)
  probs = model.predict(x_vec)
  preds = tf.cast(tf.round(probs), tf.int32)
  preds = tf.squeeze(preds).numpy().tolist()
  pred_data = pd.DataFrame.from_dict({'review': np.squeeze(x, axis=-1), 'predictions': preds}, )

  return pred_data.to_json(orient='records')


app = Flask(__name__)

@app.route("/predict", methods=['GET',"POST"])
def index():

  request_json = request.get_json()
  x = request_json['input']
  prediction = predict(x)
  response = {'prediction':int(prediction)}
  return jsonify(response), 201

@app.route("/predictions", methods=['GET',"POST"])
def predictions():
  try:
    file = request.files['file']
  except:
    return jsonify({'error': 'could not read file'})

  df = pd.read_csv(file)
  response = predict_csv(df)

  return response, 201



if __name__ == '__main__':
  app.run(debug=True)