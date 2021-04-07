import talib
import yfinance as yf
from datetime import datetime
print(str(datetime.now()).split()[0])
data = yf.download("SPY", start="2021-03-01", end=str(datetime.now()).split()[0])
print(data)
morning_star = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])

engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

data['Morning Star'] = morning_star
data['Engulfing'] = engulfing

engulfing_days = data[data['Engulfing'] != 0]

# print(engulfing_days)
# print(datetime.now())