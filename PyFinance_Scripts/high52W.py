import pandas as pd
import yfinance as yf
from getTickers import nifty200tickers,nifty50tickers,nifty100tickers
from datetime import datetime,timedelta
import warnings
from fetchDataCSV import fetchDataCSV
warnings.simplefilter(action='ignore', category=Warning)

tickers=["{}.NS".format(tick) for tick in nifty100tickers()]

data_file='Datasets/TTMSQZ-Nifty100.csv'
from_date=datetime.today()-timedelta(365)

df = fetchDataCSV(tickers=tickers,data_file=data_file,from_date=from_date)

pct_check=10
multiplier=((100-pct_check)/100)
i=1
for tick in df.Symbol.unique():
    
    df1=df[df['Symbol']==tick]
    
    close=round(df1.iloc[-1]['Close'],2)
    high52=round(df1['Close'].max(),2)
    
    if close >= high52*multiplier:
        diff=close - high52
        pct_chg=round(abs(diff)/high52*100,2)
        if diff == 0 :
            print("{}. {} is trading at {} ; it's new 52W High - {}\n".format(i,tick,close,high52))
            i+=1
        elif diff < 0:
            print("{}. {} is trading at {} : {} % below it's 52W High - {}\n".format(i,tick,close,pct_chg,high52))
            i+=1

        

