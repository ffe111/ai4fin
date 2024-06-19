"""
insvesting.py 
scraping news data from investing
 - scraping topic article✔
 - sentiment ✔
 - scraping date
   <time data-test="article-publish-date" datetime="2024-03-20 18:57:17" 
   class="ml-2"> 2h ago</time>
 - input time for scraping 
"""

import requests
from bs4 import BeautifulSoup
import js2py
import re
from sentiment import *
import sys


def requesting(url):
    try:
        res = requests.get(url, timeout=5)
        res.encoding = "utf-8"

        if res.status_code == 200:
            print("Successful\n")
            return res.text
        elif res.status_code == 404:
            xcpn = "Error 404 page not found\n"
            sys.exit(f"error request: {xcpn}")
        else:
            xcpn = "Not both 200 and 404\n"
            sys.exit(f"error request: {xcpn}")
    except Exception as xcpn:
        sys.exit(f"error request: {xcpn}")


def scraping(url):
    res = requesting(url)
    try:
        if res != None:
            soup = BeautifulSoup(res, 'html.parser')
            #  regex = re.compile('block w-full sm:flex-1')
            #  result = soup.find_all('div', {'class': regex})
            #  print(soup)
            result = soup.find('div', class_='mb-4')
            #  print(result)

            article = re.compile('article-title-link')
            # news_title = result.find_all('a', {'data-test': article})
            # date = re.compile('article-publish-date')
            # news_date = result.find_all('time', {'data-test': date})
            # for i in news_title:
            #     print(type(i))

            for news_item in result:
                news_item
            news_headlines = []
            for news_item in result.find_all('a', {'data-test': article}):
                headline = news_item.text.strip()
                news_headlines.append(headline)
            return news_headlines
    except Exception as xcpn:
        sys.exit(f"error scraping: {xcpn}")


if __name__ == "__main__":
    url = "https://www.investing.com/commodities/crude-oil-news"
    # scraping(url)
    sentiment = [{new: estimate_sentiment(new)}
                 for new in scraping(url) if new != None]
    print(sentiment)
