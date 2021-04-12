import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM
import pickle
import joblib
import warnings
warnings.filterwarnings("ignore")

import random
from sklearn.metrics import mean_squared_error
from math import sqrt
# from sklearn.externals import joblib
def create_model():
    model = Sequential()
    model.add(LSTM(units=128, activation='tanh', kernel_initializer=tf.keras.initializers.glorot_uniform(seed=26), input_shape = (61,1)))
    model.add(Dense(1, name="output_layer"))
    return model


minmax = joblib.load('min_max.pickle')

def prediction_single_day(date):  #date: Enter date for which you want next day's price prediction.
    
    #Loading Data
    data = pd.read_csv('final_tweet_score.csv')
    # with open('min_max.pickle', 'rb') as i:
    #     minmax = pickle.load(i)

    #Predicting
    data['price'] = minmax.transform(data['price'].values.reshape(-1, 1))

    model = create_model()
    model.load_weights('LSTM_with_Sentiments.h5')

    try:
        present_day = data[data['date'] == date].index[0]
        print(present_day)
        last_60_days_price = data['price'][present_day-59:present_day+1].values
        last_day_news_score = data[data['date'] == date]['score']

        prediction_array = np.append(last_60_days_price, last_day_news_score).reshape(-1, 1)
        prediction_array = np.expand_dims(prediction_array, axis=0)
        
        print("Predicting Next Working Day's Nifty 50 Index Price...\n")

        predicted_stock_price = model.predict(prediction_array)
        predicted_stock_price = minmax.inverse_transform(predicted_stock_price)
        predicted_stock_price = predicted_stock_price[0][0]

        actual_price = data['price'][present_day]
        actual_price = minmax.inverse_transform([[actual_price]])
        actual_price = actual_price[0][0]

        print(f'Predicted Index Price for the next working day after {date}: {predicted_stock_price}')
        # print(f'Actual Index Price for the next working day after {date}: {actual_price}\n')

    except (IndexError, UnboundLocalError):
        print('Entered Date should lie between period 2015-01-01 and 2019-12-31 and should not lie on a stock market holiday. Please enter a correct date.')

    except:
        print('Invalid Date Format. Please put date in yyyy-mm-dd format.')

prediction_single_day('2021-04-12') 

def prediction_multiple_days():

    #Loading Data
    data = pd.read_csv('final_tweet_score.csv')
    minmax = joblib.load('min_max.pickle')
    #with open('min_max.pickle', 'rb') as i:
     #   minmax = pickle.load(i)

    #Predicting
    data['price'] = minmax.transform(data['price'].values.reshape(-1, 1))
    
    prediction_prices = []
    actual_prices = []

    # random.seed(20)
    # n = random.randint(0, len(data)-60)
    n = len(data)-60
    random_date = data['date'][n]
    print(random_date )
    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    # random_date = '2021-04-06'
    
    print(f'Predicting for next 60 days from date: {random_date}')

    model = create_model()
    model.load_weights('LSTM_with_Sentiments.h5')

    for i in range(n, n+60):
        date = data['date'][i]

        present_day = data[data['date'] == date].index[0]

        last_60_days_price = data['price'][present_day-59:present_day+1].values
        last_day_news_score = data[data['date'] == date]['score']

        prediction_array = np.append(last_60_days_price, last_day_news_score).reshape(-1, 1)
        prediction_array = np.expand_dims(prediction_array, axis=0)

        predicted_stock_price = model.predict(prediction_array)
        predicted_stock_price = minmax.inverse_transform(predicted_stock_price)
        predicted_stock_price = predicted_stock_price[0][0]

        actual_price = data['price'][present_day]
        actual_price = minmax.inverse_transform([[actual_price]])
        actual_price = actual_price[0][0]

        prediction_prices.append(predicted_stock_price)
        actual_prices.append(actual_price)

    plt.figure(figsize=(12,7))
    plt.plot(prediction_prices, color = 'red', label = 'Predicted Prices')
    plt.plot(actual_prices, color = 'green', label = 'Actual Prices')
    plt.title('Nifty Index Prediction for 60 Consecutive Days')
    plt.xlabel('Days')
    plt.ylabel('Prices')
    plt.legend()
    plt.show()

    RMSE = sqrt(mean_squared_error(prediction_prices, actual_prices))
    print(f"RMSE: {RMSE}")


#prediction_multiple_days()