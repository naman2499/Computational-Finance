import pandas as pd
import pandas_datareader as web
import datetime as dt
from datetime import datetime
company = '^NSEI'
start = dt.datetime(2018, 1, 1)
end = datetime.now()
# print(end)
data = web.DataReader(company, 'yahoo', start, end)
data = data.drop(labels = {'High','Low',"Open",'Volume',"Adj Close"},axis = 1)
# data.columns = ['date' , 'price']
data.rename(columns = {'Date': 'date' , 'Close' : 'price'}, inplace = True)
data.to_csv('nifty_last60.csv')

print(data)
