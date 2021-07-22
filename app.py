import streamlit as st
import pandas as pd
from google.cloud import storage
import utils
import os
import json

dev = False

if dev:
    URL_PREDICTIONS = "http://127.0.0.1:5000/predictions"
    URL_PREDICT = "http://127.0.0.1:5000/predict"
else:
    URL_PREDICT  =  "https://food-nlp-g5yr3ihzpq-uw.a.run.app/predict"
    URL_PREDICTIONS = "https://food-nlp-g5yr3ihzpq-uw.a.run.app/predictions"


BUCKET_NAME = 'food-nlp-data'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "calm-spring-320419-39eded0b835c.json"

st.markdown("<h1 style='text-align: center; color:#295E61 ;'>Restaurant 5 Star Review Classification</h1>",
            unsafe_allow_html=True)


options = ('Single Review','CSV File')
mode = st.sidebar.selectbox("What mode", options)


if options[0] == mode:

    review = st.text_input('Enter review here...')

    if review:
        if review.isnumeric():
            st.warning("Please enter text. Not a number")
        else:
            try:
                resp = utils.get_predict(URL_PREDICT, review)
                st.json(resp)
            except:
                st.warning("Connection timed out. Try again")




if options[1] == mode:

    st.write("Upload CSV file filled with unlabeled reviews")
    uploaded_file = st.file_uploader(label="Upload CSV", type=["csv"])

    if uploaded_file:

        # Convert to JSON and send to Flask server
        df = pd.read_csv(uploaded_file)
        json_data = df.to_json(orient='records')
        resp = utils.get_predictions(URL_PREDICTIONS, json_data)

        pred_df = pd.DataFrame(resp)
        st.dataframe(pred_df.head())

        blob_name = f"{uploaded_file.name.split('.')[0]}_predictions.csv"
        ## upload to GCS
        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(blob_name, chunk_size=262144)
        blob.upload_from_string(pred_df.to_csv(index=False), 'text/csv')
        st.success('CSV Saved to GCS')
        ## fix type error expected str bytes or os.pathlike object not uploadedfile