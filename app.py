import streamlit as st
import pandas as pd
import requests
import utils

URL_PREDICT  =  "http://127.0.0.1:5000/predict"

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
                resp = utils.get_prediction(URL_PREDICT, review)
                st.json(resp)
            except:
                st.warning("Connection timed out. Try again")




if options[1] == mode:

    st.write("Upload CSV file filled with unlabeled reviews")
    uploaded_file = st.file_uploader(label="Upload CSV file", type=["csv"])

    if uploaded_file:

        # resp = utils.get_predictions("http://127.0.0.1:5000/predictions", )
        # st.json(resp)

        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        ## fix type error expected str bytes or os.pathlike object not uploadedfile