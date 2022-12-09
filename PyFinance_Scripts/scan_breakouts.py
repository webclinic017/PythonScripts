#!/usr/bin/env python
# coding: utf-8

from sys import implementation
import pandas as pd
import yfinance as yf
from datetime import datetime,timedelta
import time
import plotly.graph_objects as go
from get_histdata import GetHistData_yf
from fetchDataCSV import fetchDataCSV
import warnings
warnings.simplefilter(action='ignore', category=Warning)
from plot_it import plot_it


def is_consolidating(df,period=15,percentage=2.5):
    '''This functions scans the dataframe with historical values for stocks that are consolidating.
    usage: is_consolidating(df,period=15,percentage=2.5)
    returns Boolean
    ----------------------------
    (df_in, pd.DataFrame)        : A pandas DataFrame containing 'Close' column with closing prices for the required period.
    (period, int, optional)      : period of scan. default is 15 days.
    (pct_chg, float, optional)   : Percentage change in close prices for the period provided. default is 2.5%.
                                   stock whose close price in past 10 days or the period provided is below 
                                   2.5% of the max close price in this range (consolidating).
    ----------------------------
    returns Boolean              True - if a stock is consolidating
                                 False - otherwise
    '''
    recent_closes=df[-period:]['Close']
    max_close=recent_closes.max()
    min_close=recent_closes.min()
    
    if df.shape[0]<period:
        return False
    
    threshold=1-(percentage/100)
    if min_close > (threshold*max_close):
        return True
    return False

def is_breakingout(df,period=15,percentage=2.5):
    '''This functions scans the dataframe with historical values for stocks that are breaking out of consolidation.
    usage: is_breakingout(df,period=15,percentage=2.5)
    returns Boolean
    ----------------------------
    (df_in, pd.DataFrame)        : A pandas DataFrame containing 'Close' column with closing prices for the required period.
    (period, int, optional)      : period of scan. default is 15 days.
    (pct_chg, float, optional)   : Percentage change in close prices for the period provided. default is 2.5%.
                                   stock whose close price in past 10 days or the period provided is below 
                                   2.5% of the max close price in this range (consolidating).
    ----------------------------
    returns Boolean              True - if a stock is is_breakingout
                                 False - otherwise
    '''

    last_close=df[-1:]['Close'][0]
    
    if is_consolidating(df[:-1],period,percentage):
        recent_closes=df[-(period+1):-1]['Close']
        if last_close > recent_closes.max():
            return True
    return False


def daily_scan(df_in,period=10,pct_chg=2.5,plotit=False):
    '''This functions scans the dataframe with historical values for stocks that are breaking out or consolidating.
    usage: daily_scan(df_in,period=10,pct_chg=2.5)
    returns 2 lists
    ----------------------------
    (df_in, pd.DataFrame)        : A pandas DataFrame containing 'Close' column with closing prices for the required period.
                                   df_in should also have a column 'Symbol' which contains stock tickers.
    (period, int, optional)      : period of scan. default is 10 days.
    (pct_chg, float, optional)   : Percentage change in close prices for the period provided. default is 2.5%.
                                   stock whose close price in past 10 days or the period provided is below 
                                   2.5% of the max close price in this range (consolidating).
    (plotit, Bool, optional)     : Plot the candlestick chart with Plotly. default is False.
    ----------------------------
    returns 2 lists              list 1 = list of consolidating stocks.
                                 list 2 = list of stocks that are breaking out.
    '''
    
    rows=period+5
    cons_stock_list=[]
    breaking=[]
    tickers=df_in['Symbol'].unique()
    for i,tick in enumerate(tickers):
        df1=df_in[df_in['Symbol']==tick]
        df=df1[-rows:]
        if not df.empty:
           
            if is_consolidating(df,period,pct_chg):
                cons_stock_list.append(tick)
                if plotit:
                    plot_it(df1)

            if is_breakingout(df,period,pct_chg):
                breaking.append(tick)
                if plotit:
                    plot_it(df1)
                
    return cons_stock_list,breaking


def main():


    # Variables for yfinance
    look_back=45 #days ago
    look_upto=0 #days ago; 0=today
    uptrend_period=3 #days
    interval='1d' 

    to_date=(datetime.today()-timedelta(look_upto)).strftime("%Y-%m-%d")
    from_date=(datetime.today()-timedelta(look_back)).strftime("%Y-%m-%d")
    # Convert string datetime to datetime datatype
    to_date=datetime.strptime(to_date,"%Y-%m-%d")
    from_date=datetime.strptime(from_date,"%Y-%m-%d")


    # In[3]:


    data=pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')[1]
    tickers=data['Symbol'].to_list()
    tickers=["{}.NS".format(tick) for tick in tickers]
    data_file='Datasets/Nifty50_brkouts.csv'

    # In[4]:
    df=fetchDataCSV(tickers,data_file,datetime.today()-timedelta(180))
    cons,brk=daily_scan(df,plotit=True)
    print("Consolidating stocks: {}".format(cons))
    print("Breakout stocks: {}".format(brk))

if __name__=="__main__":
    main()



