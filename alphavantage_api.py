import requests
import json
import datetime
from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.getenv("alphavantageapi")


class StockAPI():
    def __init__(self, ticker:str="tsla") -> None:
        self.ticker = ticker

    def __apicall(self):
            
        url = "https://www.alphavantage.co/query?"

        params={
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": self.ticker,
            "interval": "30min",
            "apikey": api_key
        }

        response = requests.get(url=url, params=params).json()
        return response




    def get_data(self):
        data = self.__apicall()
        formatted_data = {
            'Meta data': {
                'symbol': data['Meta Data']['2. Symbol'],
                'last refreshed': data['Meta Data']['3. Last Refreshed'],
                'time zone': data['Meta Data']['5. Time Zone']
            },
            'data': []
            }
        
        for x in data['Time Series (Daily)']:
            # date = datetime.datetime(int(x[0:4]), int(x[5:7]), int(x[8:10]))
            date = x
            open = float(data['Time Series (Daily)'][x]['1. open'])
            high = float(data['Time Series (Daily)'][x]['2. high'])
            low = float(data['Time Series (Daily)'][x]['3. low'])
            close = float(data['Time Series (Daily)'][x]['4. close'])
            diff_price = round(close-open, 2)
            diff_price_percent = round(((open-close)/open)*100, 2)
            volume = int(data['Time Series (Daily)'][x]['6. volume'])
            # print(datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10])))
            
            temp_dict = {
                'date': date,
                'open': open,
                'high': high,
                'low': low,
                'close': close,
                'price difference': diff_price,
                'percentage difference': diff_price_percent,
                'volume': volume
                }
            formatted_data['data'].append(temp_dict)

        return formatted_data
    
