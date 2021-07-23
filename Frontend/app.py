import streamlit as st
import pandas as pd
from google.cloud import storage
import utils
import os
import gcsfs
from oauth2client.service_account import ServiceAccountCredentials


dev = True

if dev:
    URL_PREDICT  =  "https://food-nlp-g5yr3ihzpq-uw.a.run.app/predict"
    URL_PREDICTIONS = "https://food-nlp-g5yr3ihzpq-uw.a.run.app/predictions"
    BUCKET_NAME = 'food-nlp-data'
    PROJECT_NAME = 'calm-spring-320419'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "calm-spring-320419-39eded0b835c.json"


else:
    URL_PREDICT  =  os.environ.get('URL_PREDICT')
    URL_PREDICTIONS = os.environ.get('URL_PREDICTIONS')
    PROJECT_NAME = 'calm-spring-320419'
    BUCKET_NAME = 'food-nlp-data'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"


options = ('Single Review','CSV File', "Data Analysis")
mode = st.sidebar.selectbox("What mode", options)


if options[0] == mode:
    st.markdown("<h1 style='text-align: center; color:#295E61 ;'>Restaurant 5 Star Review Classification</h1>",
                unsafe_allow_html=True)

    st.write("""This website hosts a LSTM Neural Network pretrained and fine tuned on the 300 dimensional Glove Embeddings. 
    The model was trained around 1 million reviews and ratings that were scrapped of Tripadvisor.com.
    It is a classification algorithm which outputs a 1 for a 5 star review and a 0 for anything else""")
    review = st.text_input('Enter review here...')

    if review:
        if review.isnumeric():
            st.warning("Please enter text. Not a number")
        else:
            try:
                resp = utils.get_predict(URL_PREDICT, review)
                if resp['prediction'] == 1:
                    st.header("That was a five star review")
                else:
                    st.header("Not quite good enough for 5 stars")


            except:
                st.warning("Connection timed out. Try again")




if options[1] == mode:

    st.markdown("<h1 style='text-align: center; color:#295E61 ;'>Restaurant 5 Star Review Classification</h1>",
                unsafe_allow_html=True)
    st.write("""This website hosts a LSTM Neural Network pretrained and fine tuned on the 300 dimensional Glove 
    Embeddings. 
       The model was trained around 1 million reviews and ratings that were scrapped of Tripadvisor.com.
       It is a classification algorithm which outputs a 1 for a 5 star review and a 0 for anything else""")

    st.write("Upload CSV file filled with unlabeled reviews")
    uploaded_file = st.file_uploader(label="Upload CSV", type=["csv"])

    if uploaded_file:

        # Convert to JSON and send to Flask server
        df = pd.read_csv(uploaded_file)
        json_data = df.to_json(orient='records')
        resp = utils.get_predictions(URL_PREDICTIONS, json_data)

        pred_df = pd.DataFrame(resp)
        st.write("Preview of Predictions")
        st.dataframe(pred_df.head())

        upload = st.selectbox("Upload to GCS", ("No", "Yes"))

        if upload == "Yes":
            blob_name = f"{uploaded_file.name.split('.')[0]}_predictions.csv"
            path = f"output_data/{blob_name}"
            ## upload to GCS
            client = storage.Client()
            bucket = client.get_bucket(BUCKET_NAME)
            blob = bucket.blob(path, chunk_size=262144)
            blob.upload_from_string(pred_df.to_csv(index=False), 'text/csv')
            st.success("File Uploaded to Cloud Storage")


if options[2] == mode:

    @st.cache
    def load_data():
        fs = gcsfs.GCSFileSystem(project= PROJECT_NAME)
        with fs.open("food-nlp-data/train_test_val_data/no_reviews.csv") as f:
            df = pd.read_csv(f)
        return df


    st.markdown("<h1 style='text-align: center; color:#295E61 ;'>Restaurant Review Data Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left; color:#295E61 ;'>Numerical Plots</h3>", unsafe_allow_html=True)
    df = load_data()
    st.pyplot(utils.plot_hists(df))
    st.write("""Ratings are skewed to the left. The average review is 4.23 despite the max being a 5. The median being a 5 indicates that, at least 50 percent of reviews are 5 stars. 
                To mitigate the class imbalance, the ratings column was transformed to 5 star or not 5 star.""")

    st.markdown("<h3 style='text-align: left; color:#295E61 ;'>Categorical Plots</h3>", unsafe_allow_html=True)
    st.pyplot(utils.plot_cats(df))
    st.write("""La Puerta restaurant contains little over 30,000 reviews out of the million collected. This imbalance can lead to classification algorithim to overtrain on La Puerta's reviews.
                    A worthy experiment could be to randomly remove reviews of restaurant's who has over a certain number of reviews""")



