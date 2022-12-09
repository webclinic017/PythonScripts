#!/usr/bin/env python
# coding: utf-8

# In[4]:


from nsepy import get_history
from datetime import datetime,timedelta
#import talib as tb
import pandas as pd
import time


# In[10]:


period=30 #days
uptrend_period=1 #days
to_date=datetime.now()
from_date=(datetime.today()-timedelta(period))
from_date,to_date


# In[11]:

print("Getting Nifty50 stocks from wikipedia...")
N50_symbols=pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')[1]
print("Import successful!!")
tickers=N50_symbols['Symbol'].to_list()

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


# In[89]:

print("Printing continuous {} days uptrends.".format(uptrend_period))
for ticker in tickers:
    print(ticker)
    count=0
    up_trend=0
    data=hist_N50[hist_N50['Symbol']==ticker]
    for i,close in enumerate(data['Close']):
        if data['Close'][i]>data['Open'][i]:
            if count == 0:
                start_1=data['Close'].index[i]
                start_val_1=data['Close'][i]
            count+=1  
        elif data['Close'][i]>(data['Close'][i-1]+data['Open'][i-1])/2:
            continue;
        else:
            if count<uptrend_period:
                count=0
            else:
                up_trend+=1
                end_1=data['Close'].index[i-1]
                end_val_1=data['Close'][i-1]
                # Calculate % increase during this uptrend
                chg_p=(data.loc[end_1,'Close']-data.loc[start_1,'Close'])/data.loc[start_1,'Close']*100
                print("from {} to {} : {}% [{} > {}]".format(start_1,end_1,round(chg_p,3),start_val_1,end_val_1))
                count=0

    print("====================")
        

