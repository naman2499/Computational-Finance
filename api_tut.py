import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import unirest
from matplotlib import rcParams
unirest.timeout(15) # 5s timeout
RAPIDAPI_KEY  = "796182163dmshcd58bcfab2ec8e4p1fd9b6jsn5594a3b1a02e" 
RAPIDAPI_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"
symbol_string = ""
inputdata = {}
def fetchStockData(symbol):
  
  response = unirest.get("https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts?region=US&lang=en&symbol=" + symbol + "&interval=1d&range=3mo",
    headers={
      "X-RapidAPI-Host": 'apidojo-yahoo-finance-v1.p.rapidapi.com',
      "X-RapidAPI-Key": '796182163dmshcd58bcfab2ec8e4p1fd9b6jsn5594a3b1a02e',
      "Content-Type": "application/json"
    }
  )
  
  if(response.code == 200):
    return response.body
  else:
    return None
def parseTimestamp(inputdata):
  timestamplist = []
  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
  calendertime = []
  for ts in timestamplist:
    dt = datetime.fromtimestamp(ts)
    calendertime.append(dt.strftime("%m/%d/%Y"))
  return calendertime
def parseValues(inputdata):
  valueList = []
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])
  return valueList
def attachEvents(inputdata):
  eventlist = []
  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventlist.append("open")  
  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventlist.append("close")
  return eventlist
if __name__ == "__main__":
  try:
    while len(symbol_string) <= 2:
      symbol_string = raw_input("Enter the stock symbol: ")
    retdata = fetchStockData(symbol_string)
    
    if (None != inputdata): 
      inputdata["Timestamp"] = parseTimestamp(retdata)
      inputdata["Values"] = parseValues(retdata)
      inputdata["Events"] = attachEvents(retdata)
      df = pd.DataFrame(inputdata)
      sns.set(style="darkgrid")
      rcParams['figure.figsize'] = 13,5
      rcParams['figure.subplot.bottom'] = 0.2
      
      ax = sns.lineplot(x="Timestamp", y="Values", hue="Events",dashes=False, markers=True, 
                   data=df, sort=False)
      ax.set_title('Symbol: ' + symbol_string)
      
      plt.xticks(
          rotation=45, 
          horizontalalignment='right',
          fontweight='light',
          fontsize='xx-small'  
      )
      plt.show()
  except Exception as e:
    print ("Error")   
    print (e)
