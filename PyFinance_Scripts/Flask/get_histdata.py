#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import yfinance as yf
from nsepy import get_history
from datetime import datetime,timedelta
import time
import sys


def GetHistData_yf(tickers,start=None,end=None,interval='1d'):
    '''This function retrieves historical data of the list of tickers provided.
    GetHistData_yf(tickers,start=None,end=None,interval='1d')
    returns a DataFrame
    ---------------------------------
    (tickers, list)                   = A list containg ticker symbols as listed yfinance.
                                        Ex. ['ADANIPORTS.NS','TCS.NS','LT.NS','AXISBANK.NS',]
    (start, datetime or str,optional) = Start date of historical data. default is 3 months from current date.
                                        ex. '2021-08-01' 
    (end, datetime or str,optional)   = End date of historical data. default is current date.
                                        ex. '2022-08-01'
    (interval, string, optional)      = The price interval. default is 1 day.
                                        ex. '1d', '1h', '5m'
    ---------------------------------
    returns  - A dataframe containg historic data for the ticker provided for the range provided.
    This function uses yfinance module
    '''
    
    if start==None:
        from_date=datetime.strptime((datetime.today()-timedelta(90)).strftime("%Y-%m-%d"),"%Y-%m-%d")
    elif type(start) == str:
        from_date=datetime.strptime(start,"%Y-%m-%d")
    else:
        from_date=datetime.strptime(start.strftime("%Y-%m-%d"),"%Y-%m-%d")     
    
    if end==None:
        # the yf API is not providing current day's data even when to_date is specified as .today()
        # but fetching latest data when left blank
        # to_date=datetime.strptime(datetime.today().strftime("%Y-%m-%d"),"%Y-%m-%d") 
        to_date=None
    elif type(end) == str:
        to_date=datetime.strptime(end,"%Y-%m-%d")
    else:
        to_date=end

        
    start_time = time.time()
    hist_data=pd.DataFrame()
    # Get historical data
    print("Getting historical using yfinance")
    print("Fetching data from {} to {}".format(from_date,to_date))
    hist_data=pd.DataFrame()
    for i,tick in enumerate(tickers):
        if i == 0 :
            hist_data=yf.download("{}".format(tick),start=from_date,end=to_date,interval=interval)
            if not hist_data.empty:
                hist_data['Symbol']=tick
        else :
            df2=yf.download(tick,start=from_date,end=to_date,interval=interval)
            if not df2.empty:
                df2['Symbol']=tick
                if hist_data.empty:
                    hist_data=df2
                else:
                    hist_data=pd.concat([hist_data,df2])

    print("--- %s seconds ---" % (time.time() - start_time))
    return hist_data

def GetHistData_nse(tickers,start=None,end=None):
    '''This function retrieves historical data of the list of tickers provided.
    GetHistData_yf(tickers,start=None,end=None)
    returns a DataFrame
    ---------------------------------
    (tickers, list)                   = A list containg ticker symbols as listed yfinance.
                                        Ex. ['ADANIPORTS.NS','TCS.NS','LT.NS','AXISBANK.NS',]
    (start, datetime or str,optional) = Start date of historical data. default is 3 months from current date.
                                        ex. '2021-08-01' 
    (end, datetime or str,optional)   = End date of historical data. default is current date.
                                        ex. '2022-08-01'
    ---------------------------------
    returns  - A dataframe containg historic data for the ticker provided for the range provided.
    This function uses nsepy module
    '''
    if start==None:
        from_date=datetime.strptime((datetime.today()-timedelta(90)).strftime("%Y-%m-%d"),"%Y-%m-%d")
    elif type(start) == str:
        from_date=datetime.strptime(start,"%Y-%m-%d")
    else:
        from_date=datetime.strptime(start.strftime("%Y-%m-%d"),"%Y-%m-%d")     
    
    if end==None:
        to_date=datetime.strptime(datetime.today().strftime("%Y-%m-%d"),"%Y-%m-%d") 
    elif type(end) == str:
        to_date=datetime.strptime(end,"%Y-%m-%d")
    else:
        to_date=end

    start_time = time.time()
    hist_N50=pd.DataFrame()

    # Get historical data
    print("Getting historical using nsepy API")
    print("Fetching data from {} to {}".format(from_date,to_date))
    for i,ticker in enumerate(tickers):
        if i == 0 :
            hist_N50=get_history(symbol=ticker,start=from_date,end=to_date)
        else :
            df2=get_history(symbol=ticker,start=from_date,end=to_date)
            hist_N50=pd.concat([hist_N50,df2])

    print("--- %s seconds ---" % (time.time() - start_time))
    return hist_N50

if __name__=="__main__":
    argList = sys.argv[1:]
    print(argList)
    print(GetHistData_yf(argList))
