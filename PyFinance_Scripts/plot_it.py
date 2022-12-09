import warnings
warnings.simplefilter(action='ignore', category=Warning)
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def plot_it(df1):
    '''Plots a candlestick chart for the dataframe provided. Also draws the 21,34,55,89 Simple moving averages.
    (df1, pd.DataFrame)     : A pandas dataframe containg columns Open, High, Low, Close
    _____________________________________________
    returns nothing. ( returns a bool True, just as a formality. what will you do with it?)
    '''
    candlestick=go.Candlestick(x=df1.index,open=df1['Open'], high=df1['High'],low=df1['Low'],close=df1['Close'])
    df1['21sma']=df1['Close'].rolling(window=21).mean()
    df1['34sma']=df1['Close'].rolling(window=34).mean()
    df1['55sma']=df1['Close'].rolling(window=55).mean()
    df1['89sma']=df1['Close'].rolling(window=89).mean()
    
    sma21=go.Scatter(x=df1.index,y=df1['21sma'],name='21sma', line={'color':'blue'})
    sma34=go.Scatter(x=df1.index,y=df1['34sma'],name='34sma', line={'color':'green'})
    sma55=go.Scatter(x=df1.index,y=df1['55sma'],name='55sma', line={'color':'yellow'})
    sma89=go.Scatter(x=df1.index,y=df1['89sma'],name='89sma', line={'color':'red'})

    fig = go.Figure(data=[candlestick,sma21,sma34,sma55,sma89])
    fig.update_layout(title='{}'.format(df1['Symbol'].unique()[0]))
    fig.layout.xaxis.type='category'
    fig.layout.xaxis.rangeslider.visible=False

    fig.show()
    return True
