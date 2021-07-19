import pickle
import concurrent.futures
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
import numpy as np

from flask import Flask, request, jsonify


pickle_path = "tv_layer.pkl"
model_path = 'lstm_finetune_novec.h5'

def load_vectorizer(path):
  from_disk = pickle.load(open(path, "rb"))
  loaded_vectorizer = TextVectorization.from_config(from_disk['config'])
  loaded_vectorizer.set_weights(from_disk['weights'])
  return loaded_vectorizer


def load_model_vectorizer(model_path, pickle_path):
    with concurrent.futures.ThreadPoolExecutor() as executor:
      f1 = executor.submit(tf.keras.models.load_model, model_path)
      f2 = executor.submit(load_vectorizer, pickle_path)
      loaded_model = f1.result()
      loaded_vectorizer = f2.result()

      return loaded_model, loaded_vectorizer


model, vectorizer = load_model_vectorizer(model_path, pickle_path)

def predict(sentence):
  x_vec = vectorizer(np.array([sentence]))
  prob = model.predict(x_vec)[0]

  return tf.round(prob).numpy()[0]


app = Flask(__name__)

@app.route("/predict", methods=['GET',"POST"])
def index():

  request_json = request.get_json()
  x = request_json['input']
  prediction = predict(x)
  response = {'prediction':int(prediction)}
  return jsonify(response), 201



if __name__ == '__main__':
  app.run(debug=True)