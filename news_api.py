import requests
from dotenv import load_dotenv
import os 
from datetime import date
import datetime


date_today = str(datetime.datetime.today() - datetime.timedelta(days=1))[:10]



load_dotenv()
api_key = os.getenv("newsapi")

class NewsAPI():
    def __init__(self, ticker:str="tsla") -> None:
        self.ticker = ticker
        

    def api_call(self):
        url = f"https://newsapi.org/v2/everything?q={self.ticker}&from={date_today}&sortBy=publishedAt&apiKey={api_key}&language=en&pageSize=100"
        data = requests.get(url).json()
        print(data)
        ls_data = []
        for x in data['articles']:
            temp_dic = {
                "author": x['author'],
                "title": x['title'],
                "description": x['description'],
                "url": x['url'],
                "publishedAt": x['publishedAt']
            }
            ls_data.append(temp_dic)
        return ls_data



