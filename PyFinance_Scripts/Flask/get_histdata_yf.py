#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime,timedelta
import time
import sys

# In[10]:


def GetHistData_yf(tickers,start=None,end=None,interval='1d'):
    '''This function retrieves historical data of the list of tickers provided.
    GetHistData_yf(tickers,start=None,end=None,interval='1d')
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
    returns hist_data  - A dataframe containg historic data for the ticker provided for the range provided.
    '''
    
    if start==None:
        from_date=(datetime.today()-timedelta(90)).strftime("%Y-%m-%d")
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
    hist_data=pd.DataFrame()
    # Get historical data
    print("Getting historical using yfinance")
    print("Fetching data from {} to {}".format(from_date,to_date))

    for i,tick in enumerate(tickers):
        security=yf.Ticker(tick)
    #     print(i,tick)
    #     print(security.splits)
        if i == 0 :
            hist_data=security.history(start=from_date,end=to_date,interval=interval)
            hist_data['Symbol']=tick
        else :
            df2=security.history(start=from_date,end=to_date,interval=interval)
            if not df2.empty:
                df2['Symbol']=tick
                hist_data=pd.concat([hist_data,df2])

    print("--- %s seconds ---" % (time.time() - start_time))
    return hist_data
    
if __name__=="__main__":
    argList = sys.argv[1:]
    print(argList)
    print(GetHistData_yf(argList))
