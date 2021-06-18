import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def get_page_links(num_pages,url):
    """"Returns the the links to all the pages on the trip advisor page"""


    html = requests.get(url)
    page = bs(html.text, 'lxml')
    page_links = []
    for i in range(2, num_pages + 1):
        next_button = page.find("a", {"data-page-number": str(i)})
        try:
            next_url = 'https://www.tripadvisor.com' + next_button['href']
        except: break
        page_links.append(next_url)

        next_link = requests.get(next_url)
        page = bs(next_link.text, 'lxml')
    page_links.insert(0, url)
    return page_links


def get_restuarant_links(num_pages,url):
    """Returns all the links to restaurant pages in the specified number of pages"""

    page_links = get_page_links(num_pages,url)

    rest_links = []
    for link in page_links:
        html = requests.get(link)
        page = bs(html.text, 'lxml')
        rest = page.find_all("div", {"class": "wQjYiB7z"})
        for i in rest:
            rest_links.append('https://www.tripadvisor.com' + i.span.a['href'])

    return rest_links


def get_review_info(link):
    """Returns the review info (user, date, rating, review for one page"""

    html = requests.get(link)
    page = bs(html.text, 'lxml')
    try: name = page.find_all("div", {"class": "_1hkogt_o"})[0].h1.text
    except: name = link

    review_html = page.find_all('div', {'class': 'review-container'})
    ratings = []
    reviews = []
    dates = []
    user_names = []

    for container in review_html:


        review = container.find("div", {"class": "ui_column is-9"})
        rating = review.span['class'][1].split('_')[1]
        rating = int(rating)

        text_review = review.find('p', {'class': 'partial_entry'})
        try: text_review = text_review.text
        except: continue

        date = review.find('div', {'class': 'prw_rup prw_reviews_stay_date_hsx'})
        try: date = date.text.split(':')[1][1:]
        except: continue

        user_name = container.find("div", {"class": "info_text pointer_cursor"})
        try: user_name = user_name.text
        except:continue

        ratings.append(rating)
        reviews.append(text_review)
        dates.append(date)
        user_names.append(user_name)

    data = pd.DataFrame(
        {'user_name': user_names, 'rating': ratings, 'review': reviews, 'date': dates, 'restaurant': name})
    return data



def get_all_review_info(num_pages,url):
    """Returns all the review information for for every restrain in num_pages"""

    links = get_restuarant_links(num_pages,url)
    df = pd.DataFrame()
    j = 1
    for link in links:   # loops through all the restaurants main pages
        html = requests.get(link)
        page = bs(html.text, 'lxml')
        # pagination = page.find("div", {"class": "pageNumbers"})
        # try: num_pages =int(pagination.find_all('a')[-1].text)   # number of pages of reviews for a particular restaurant
        # except: continue

        data = get_review_info(link) # gets info for the first link
        df = df.append(data, ignore_index=True)

        next_page = True
        while next_page:

            next_button = page.find("a", {"class": 'nav next ui_button primary'})
            try:
                next_url = 'https://www.tripadvisor.com' + next_button['href']
            except:
                break
            data = get_review_info(next_url)
            df = df.append(data, ignore_index=True)
            print(f'{j} review pages scrapped')
            next_link = requests.get(next_url)   # gets the url to the next page of reviews
            page = bs(next_link.text, 'lxml')
            j += 1
    return df

if __name__ == "__main__":
    links = {'Los Angeles':'https://www.tripadvisor.com/Restaurants-g32655-c10646-Los_Angeles_California.html',
             'San Diego':'https://www.tripadvisor.com/Restaurants-g60750-c10646-San_Diego_California.html',
             'San Francisco':'https://www.tripadvisor.com/Restaurants-g60713-c10646-San_Francisco_California.html',
             'Orange County': 'https://www.tripadvisor.com/Restaurants-g659482-c10646-Orange_County_California.html'}

    # link = 'https://www.tripadvisor.com/Restaurants-g32655-c10646-Los_Angeles_California.html'
    # link = 'https://www.tripadvisor.com/Restaurants-g60750-c10646-San_Diego_California.html'
    # link = 'https://www.tripadvisor.com/Restaurants-g60713-c10646-San_Francisco_California.html'
    # link = 'https://www.tripadvisor.com/Restaurants-g60763-c10646-New_York_City_New_York.html'
    # link = 'https://www.tripadvisor.com/Restaurants-g60898-c10646-Atlanta_Georgia.html'
    # link = 'https://www.tripadvisor.com/Restaurants-g659482-c10646-Orange_County_California.html'

    for city, link in links.items():
        print(city)
        df = get_all_review_info(20,link)
        df.to_csv(f'{city}_restaurant.csv', index=False)



