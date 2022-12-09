import os
import pandas as pd
from get_histdata import GetHistData_yf
from getTickers import nifty200tickers,nifty50tickers,nifty100tickers
from fetchDataCSV import fetchDataCSV
import plotly.graph_objects as go
from datetime import datetime,timedelta
import warnings
warnings.simplefilter(action='ignore', category=Warning)

# 'Nifty50.csv'
data_file='Datasets/TTMSQZ-Nifty200.csv'

from_date=datetime.today()-timedelta(90)
tickers=nifty200tickers()
adj_tickers=["{}.NS".format(tick) for tick in tickers]

df = fetchDataCSV(adj_tickers,data_file,from_date)

def plot_it(df1):
    candlestick=go.Candlestick(x=df1.index,open=df1['Open'], high=df1['High'],low=df1['Low'],close=df1['Close'])
    bb_upper=go.Scatter(x=df1.index,y=df1['upperband'],name='Upper Bollinger Band', line={'color':'red'})
    bb_lower=go.Scatter(x=df1.index,y=df1['lowerband'],name='Lower Bollinger Band', line={'color':'red'})
    KC_upper=go.Scatter(x=df1.index,y=df1['upperKC'],name='Upper KC Band', line={'color':'Blue'})
    KC_lower=go.Scatter(x=df1.index,y=df1['lowerKC'],name='Lower KC Band', line={'color':'Blue'})

    fig = go.Figure(data=[candlestick,bb_upper,bb_lower,KC_upper,KC_lower])
    fig.update_layout(title='{}'.format(df1['Symbol'].unique()[0]))
    fig.layout.xaxis.type='category'
    fig.layout.xaxis.rangeslider.visible=False

    fig.show()

for tick in df['Symbol'].unique():
    df1=df[df['Symbol']==tick]

    df1['20sma']=df1['Close'].rolling(window=20).mean()
    df1['stddev']=df1['Close'].rolling(window=20).std()
    df1['lowerband']=df1['20sma'] - 2*df1['stddev']
    df1['upperband']=df1['20sma'] + 2*df1['stddev']
    
    df1['TR']=abs(df1['High']-df1['Low'])
    df1['ATR']=df1['TR'].rolling(window=20).mean()
    
    df1['upperKC']=df1['20sma'] + df1['ATR'] * 1.5
    df1['lowerKC']=df1['20sma'] - df1['ATR'] * 1.5

    def in_squeeze(df1):
        return df1['lowerband'] > df1['lowerKC'] and df1['upperband'] < df1['upperKC'] 
    
    df1['In_squeeze']=df1.apply(in_squeeze,axis=1)
    
    # and not df1.iloc[-1]['In_squeeze']
    if df1.iloc[-2]['In_squeeze']  and not df1.iloc[-1]['In_squeeze']:
        print("{} is coming out of squeeze.".format(tick))
        plot_it(df1)


