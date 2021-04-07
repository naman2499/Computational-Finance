import requests

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart"

querystring = {"interval":"5m","symbol":"AMRN","range":"1d","region":"US"}

headers = {
    'x-rapidapi-key': "796182163dmshcd58bcfab2ec8e4p1fd9b6jsn5594a3b1a02e",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)