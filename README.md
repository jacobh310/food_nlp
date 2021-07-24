# Restaurant 5 Star Natural Language Processing Classifier
---
### Project at a glance
- Scrapped over 1 million reviews along with their rating out of 5 
- Created a Natural Languauge Processing model with Tensorflow 
- Experimented with GloVe pre-trained embeddings 
- Optimized hyperparameters for 1D Convolution and LSTM architectures using Weights and Biases sweeps
- Final Model: LSTM architecture with finetuned 300 Dimensional Glove Embeddings 
- Built a client facing Streamlit web app deployed through heroku that makes API calls to Flask server hosted on Google Cloud

- Checkout the Web App: https://food-nlp.herokuapp.com/

### Code and Resources Used 
---
**Python Version:** 3.8  
**Packages:**  pandas, numpy, sklearn, matplotlib,  beautifulsoup, flask, json, pickle, tensorflow, gcloud

## Data Collection:
---
Scrapped over 1 million restuarant reviews and ratings using the beautifulsoup python library. With each review, we got the following:
- Rating out of 5
- Username
- Restaurant Name
- Date of review 

Data was scrapped for restuarants in:
- Los Angeles
- San Diego
- Orange County
- Atalanta
- New York
## Exploratory Data Analysis

