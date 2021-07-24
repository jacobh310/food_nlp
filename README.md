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
**Model Building:**  https://keras.io/examples/nlp/pretrained_word_embeddings/
**Goole Cloud Run Deployment:** https://www.youtube.com/watch?v=vieoHqt7pxo

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

## Data Cleaning and Preprocessing
---
Tensorflow offers a TextVectorization preproccessing layers that strips puncutation and lowers the case of all the letters.
Other data cleaning operations included:
-  "...More" was removed from the long reviews
-  The rating was divided by 10 to make it a out of 5 instead of 50
-  Data was split into Train/Validation/Test with a 90/5/5 split


## Exploratory Data Analysis
---
- Ratings are skewed to the left. The avverage review is 4.23 despite the max being a 5. The media being a 5 indicates that, at least 50 percent of reviews are 5 stars. To mitigate the class imbalance, the ratings column was transformed to 1 for 5 star review and 0 for non 5 star review
- More majority of the reviews are held by the popular restuaurants. This is evident when looking at the mean and the 75 percentile. The average amount of revieews per restuarant is 64.86 while the 75th percentile is only 44.
![Alt text](https://github.com/jacobh310/food_nlp/blob/master/images/histograms.JPG)
- La Puerta has almost 35,000 out of the millions reviews. Any algorithim can overfit the the reviews of La Puerta. To avoid this, we can set up a potential experimenent where a threshold is set and reviews from restuarants the suprass the threshold are randomly reviewed
![Alt text](https://github.com/jacobh310/food_nlp/blob/master/images/cat_plots.JPG)


## Model Building
---
- First lets establish some evaluatoin metrics. The data set is not severly imbalanced with 55/45 split. The main evaluation metric is F1 score but we will also be tracking accuracy, precision and recall to get a more complete picture on the model's performance
- I used Scikit Learn's Naive Bayes MultinomialNB algorithim to get a non deep neural netwrok base metrics we can aim to beat
- I used Weights and Biases for experiment trackig and hyperparamter sweeps. For faster training and hyperparameter tuning, the models in the sweeps only trained and validated on 20% of their respective datasets.
- Below are the results of the best sweeps:  
### Sweep 3
- Architecture = LSTM
- Optimizer: Adam
- Max Vocab 70000
- Pre-trained Embeddings  

![Alt text](https://github.com/jacobh310/food_nlp/blob/master/images/sweep3.JPG)

### Sweep 5
- Architecture = LSTM
- Optimizer: Adam
- Max Vocab 70000
- Embedding dimension: 300
- No Pretrained Embeddings

![Alt text](https://github.com/jacobh310/food_nlp/blob/master/images/sweep5.JPG)

# Best Model's Performance
---
I took the best performing parameters from the sweeps and trained and validated the models on the whole dataset  

![Alt text](https://github.com/jacobh310/food_nlp/blob/master/images/best_model_f1.JPG)

# Model Evaluation for best model
---
### Confusion Matrix 
![Alt text](https://github.com/jacobh310/food_nlp/blob/master/images/confusion_matrix.JPG)

### ROC curve
![Alt text](https://github.com/jacobh310/food_nlp/blob/master/images/roc_curve.JPG)

# Model Deployment
---
- I built a flask API with two endpoints. One for a single review and the other for CSV file containing multiple reviews. The flask server was Dockerized and deployed to Google Cloud Run
- For the front end, I used streamlit to build a user friendly interface
- Predictions made on a CSV file were uploaded to a Google Cloud Storage bucker to track the health of the model



