# import nest_asyncio
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import twint
import random
import re
from tqdm import tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
import numpy as np

def loadtweet_data(start_date, end_date):
    config = twint.Config()
    config.Username = "NDTVProfit"
    config.Lang = "en"
    config.Since = start_date
    config.Until = end_date
    config.Store_csv = True
    config.Output = "ndtv_profit tweets.csv"
    # running search
    twint.run.Search(config)

def process_tweet_data():
    tweet_news = pd.read_csv('ndtv_profit tweets.csv')
    print(tweet_news.shape)
    #Removing extra columns
    tweet_news = tweet_news[['date', 'tweet']]
    tweet_news = tweet_news.sort_values('date').reset_index(drop= True)
    print(tweet_news.shape)
    #Dropping duplicate values 
    # tweet_news.drop_duplicates(keep=False,inplace=True)
    print(tweet_news.shape)
    
    tweet_news.to_csv('news.csv', index = False)
    print(tweet_news.shape)



loadtweet_data("2018-01-01", "2021-04-12")
process_tweet_data()
tweet_news = pd.read_csv('news.csv')
def decontracted(phrase):
    # specific`
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def clean(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'pic.twitter\S+', ' ', text)
    text = decontracted(text)
    text = re.sub(r'\(([^)]+)\)', " ", text)
    text = text.replace('etmarkets', ' ').replace('marketupdates', ' ').replace('newsalert', ' ').replace('ndtv', ' ').replace('moneycontrol', ' ').replace('here is why', ' ')
    text = text.replace('marketsupdate', ' ').replace('biznews', ' ').replace('click here', ' ').replace('live updates', ' ').replace('et now', ' ')
    text = re.sub(r'[^a-zA-Z ]+', ' ', text)
    text = re.sub(r' \w{1,2}_', ' ', text)
    text = re.sub('\s+',' ', text)
    return text

for i in tqdm(tweet_news.itertuples()):
    tweet_news.at[i[0], 'tweet_processed'] = clean(i[2])

tweet_news['tweet_news_combined'] = tweet_news.groupby(['date'])['tweet_processed'].transform(lambda x: ' '.join(x))
tweet_news = tweet_news[['date', 'tweet_news_combined']]
tweet_news.drop_duplicates(inplace =True)
tweet_news.sort_values('date', inplace = True)
tweet_news.reset_index(drop = True)
tweet_news.to_csv('news_processed.csv', index =False)
print(tweet_news.head())

#feature enginnering
new_words =  {'falls': -9, 'drops': -9, 'rise': 9, 'increases': 9, 'gain': 9, 'hiked': -9, 'dips': -9, 'declines': -9, 'decline': -9, 'hikes': -9, 'jumps': 9,
              'lose': -9, 'profit': 9, 'loss': -9, 'shreds': -9, 'sell': -9, 'buy': 9, 'recession': -9, 'rupee weakens': -9, 'record low': -9, 'record high': 9,
              'sensex up': 9, 'nifty down': -9, 'sensex down': -9, 'nifty up': 9} 

analyser = SentimentIntensityAnalyzer()
analyser.lexicon.update(new_words)

print('starting')
tweet_news = pd.read_csv('news_processed.csv')
print(tweet_news.shape)
for i in tqdm(tweet_news.itertuples()):
    score = analyser.polarity_scores(tweet_news.iloc[i[0]]['tweet_news_combined'])

    tweet_news.at[i[0], 'score'] = score['compound']

    if score['compound'] >= 0:
        tweet_news.at[i[0], 'sentiment'] = 1
    else:
        tweet_news.at[i[0], 'sentiment'] = -1
print('yoooooooooooooo')
print(tweet_news.head())

tweet_news.to_csv('news_combined_with_sentiments.csv', index =False)
tweet_news[['date', 'sentiment']].to_csv('sentiments_final.csv', index =False)

nifty = pd.read_csv('nifty_last60.csv')
print(nifty.head())


#######combining

#Removing news for missing dates in stock price data. In Stock Price Data, data corresponding to weekend, public holidays are missing.

s = set([str(i).split('T')[0] for i in nifty['Date'].values])
n = set(list(tweet_news['date'].values))

common_dates_1 = list(n.symmetric_difference(s))

for i in tweet_news.itertuples():
    if i[1] not in [str(i).split('T')[0] for i in nifty['Date'].values]:
        tweet_news.drop(tweet_news[tweet_news['date'] == i[1]].index, inplace = True)
    else:
        pass

for j in common_dates_1:
    tweet_news.drop(tweet_news[tweet_news['date'] == j].index, inplace = True)
    nifty.drop(nifty[nifty['Date'] == j].index, inplace = True)

nifty.rename(columns = {'Date':'date'} ,inplace=True)
print(tweet_news.head())
print(nifty.head())

data1 = pd.merge(tweet_news, nifty, on = 'date')
print(data1.head())
data1.drop(labels={'tweet_news_combined'},inplace=True,axis=1)
print(data1.head())
data1.to_csv('final_tweet_score.csv')
