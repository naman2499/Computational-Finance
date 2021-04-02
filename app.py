import os, csv
import talib
import yfinance as yf
import pandas
from flask import Flask, escape, request, render_template
from patterns import candlestick_patterns
from patterns_old import candle

app = Flask(__name__)

@app.route('/snapshot')
def snapshot():
    with open('datasets/symbols.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            data = yf.download(symbol, start="2021-01-01", end="2021-02-01")
            data.to_csv('datasets/daily/{}.csv'.format(symbol))

    return {
        "code": "success"
    }

@app.route('/')
def index():
    pattern  = request.args.get('pattern', False)
    stocks = {}

    # with open('datasets/symbols.csv') as f:
        # for row in csv.reader(f):
            # stocks[row[0]] = {'company': row[1]}

    if pattern:
        print(pattern)
        # for filename in os.listdir('datasets/daily'):
        # filename = 'datasets/daily/{}'.format(pattern)
        print('YOYOYOYOYOY')
        df = pandas.read_csv('datasets/daily/{}.csv'.format(pattern))
        print('1111111YOYOYOYOYOY')
            # print('datasets/daily/{}'.format(filename))
        for each_candle in candle:
            print(each_candle)
            print("############################")
            pattern_function = getattr(talib, each_candle)
            # symbol = filename.split('.')[0]
            # symbol = pattern
            
            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = results.tail(1).values[0]
                print(last)

                if last > 0:
                    # stocks[symbol][pattern] = 'bullish'
                    stocks[each_candle] = 'bullish'
                elif last < 0:
                    # stocks[symbol][pattern] = 'bearish'
                    stocks[each_candle] = 'bearish'
                # else:
                    # stocks[symbol][pattern] = None
                    # stocks[each_candle] = 'None'
            except Exception as e:
                print('failed on filename: ', pattern, e)

    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern, candle= candle)
