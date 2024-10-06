import requests
import pandas as pd
import plotly.graph_objects as go

class StockFetch:

    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com"
        }

    def search(self, company):
        querystring = {"datatype":"json","keywords":company,"function":"SYMBOL_SEARCH"}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()["bestMatches"]
        data_dict = {}
        for i in data:
            symbol = i["1. symbol"]
            data_dict[symbol] = [i["2. name"], i["3. type"], i["4. region"]]
        
        return data_dict
    
    def daily_data(self, symbol):
        querystring = {"function":"TIME_SERIES_DAILY","symbol":symbol ,"outputsize":"compact","datatype":"json"}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()["Time Series (Daily)"]
        df = pd.DataFrame(data).T
        df.index = pd.to_datetime(df.index)
        for i in df.columns:
            df[i] = df[i].astype(float)
        return df
    
    def plot_candlestick(self, symbol):
        df = self.daily_data(symbol)
        fig = go.Figure(data= [go.Candlestick(
            x = df.index,
            open = df["1. open"],
            high = df["2. high"],
            low = df["3. low"],
            close = df["4. close"] 
        )])
        fig.update_layout(width=800, height=600)
        return fig
    
