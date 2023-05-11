import requests
import json
from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.getenv("newsapi")

class NewsAPI():
    def __init__(self, ticker:str="tsla") -> None:
        self.ticker = ticker
        

    def api_call(self):
        url = f"https://newsapi.org/v2/everything?q={self.ticker}&from=2023-04-10&sortBy=publishedAt&apiKey={api_key}&language=en&pageSize=100"
        data = requests.get(url).json()
        
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



