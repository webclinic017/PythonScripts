
from datetime import datetime
import yfinance as yf
import pandas as pd

def nifty50tickers():
    data=pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')[1]
    return data['Symbol'].to_list()


def nifty200tickers():
    data=pd.read_html('https://www.traderscockpit.com/?pageView=nse-indices-stock-watch&index=NIFTY+200')
    return data[3]['Index'].to_list()