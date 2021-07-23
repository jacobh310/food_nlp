import requests
import matplotlib.pyplot as plt


def get_predict(url, review):
    """
    Sends single review to flask server and returns with a prediction
    """
    data = {"input": review}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=data)

    return resp.json()

def get_predictions(url, json):

    """
    Sends multiple reviews from a in json format to flask server
    Returns a json with reviews an predictions
    """
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, json=json)

    return resp.json()

def clean_name(col):
    """
    Function meant to be used in dataframe apply function
    """
    if 'http' in col:
        col = col.split('Reviews')[1]
        col = col.split('-')[-2]
        col = col.replace('_',' ')
        return col
    else:
        return col


def plot_hists(df):
    review_counts = df['restaurant'].value_counts()

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))
    axes[0].hist(df['rating'])
    axes[0].set_title('Ratings Distribution',fontsize=30)
    axes[0].set_ylabel('Number of Ratings',fontsize=20)
    axes[0].set_xlabel('Rating',fontsize=20)
    axes[0].xaxis.set_tick_params(labelsize=20)
    axes[0].yaxis.set_tick_params(labelsize=15)

    axes[1].hist(review_counts, bins=18)
    axes[1].set_title('Review Counts Distribution', fontsize=30)
    axes[1].set_ylabel('Number of Restaurants',fontsize=20)
    axes[1].set_xlabel('Number of Reviews',fontsize=20)
    axes[1].xaxis.set_tick_params(labelsize=15)
    axes[1].yaxis.set_tick_params(labelsize=15)

    return fig


def plot_cats(df):

    fig = plt.figure(figsize=(30,10))

    plt.tight_layout()
    avg_rating_restaurant = df.groupby('restaurant')['rating'].mean()
    top_by_count = df['restaurant'].value_counts().head(20)

    plt.subplot(1, 2, 1)
    top_by_count.plot.bar()
    plt.title('Number of Reviews Per Most Reviewed Restaurant', fontsize=30)
    plt.ylabel('Count', fontsize=20)
    plt.xticks(rotation=30)

    plt.subplot(1,2,2)
    avg_rating_restaurant[top_by_count.index].plot.bar()
    plt.title('Average Rating per Most Reviewed Fast Food Restaurant', fontsize=30)
    plt.ylabel('Average Rating', fontsize=20)
    plt.xticks(rotation=30)




    return fig