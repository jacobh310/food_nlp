import pickle
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
import concurrent.futures


def load_vectorizer(path):
  """
  Loads a Text Vectorization object saved from Tensorflow
  """
  from_disk = pickle.load(open(path, "rb"))
  loaded_vectorizer = TextVectorization.from_config(from_disk['config'])
  loaded_vectorizer.set_weights(from_disk['weights'])
  return loaded_vectorizer


def load_model_vectorizer(model_path, pickle_path):

    """
    Loads a tensorflow model with a Text Vectorization layer
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
      f1 = executor.submit(tf.keras.models.load_model, model_path)
      f2 = executor.submit(load_vectorizer, pickle_path)
      loaded_model = f1.result()
      loaded_vectorizer = f2.result()

      return loaded_model, loaded_vectorizer


