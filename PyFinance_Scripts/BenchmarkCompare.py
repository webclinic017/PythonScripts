#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime
import yfinance as yf
import pandas as pd
from get_histdata import GetHistData_yf
from getTickers import nifty50tickers
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt # for data visualization
import plotly.graph_objects as go

import warnings
from fetchDataCSV import fetchDataCSV
warnings.simplefilter(action='ignore', category=Warning)


# In[2]:


start_time='2021-09-01'
# weights={
# 'CHAMBLFERT.NS' : 0.036,
# 'FINPIPE.NS' : 0.06,
# 'INFY.NS' : 0.03,
# 'JKLAKSHMI.NS' : 0.018,
# 'JUNIORBEES.NS' : 0.024,
# 'KIRLFER.NS' : 0.048,
# 'LT.NS' : 0.024,
# 'NIFTYBEES.NS' : 0.25,
# 'ORIENTCEM.NS' : 0.065,
# 'POLYPLEX.NS' : 0.006,
# 'REDINGTON.NS' : 0.077,
# 'SBIN.NS' : 0.042,
# 'SHK.NS' : 0.065,
# 'TATAMOTORS.NS' : 0.042,
# 'TATAPOWER.NS' : 0.149,
# 'TCS.NS' : 0.03,
# 'WIPRO.NS' : 0.036,
# }
weights={
    
    # 'HDFCBANK.NS': 0.2,
    '0P0000YWL1.BO': 1 #ParagParik Flexi
    # 'LT.NS':0.2,
    # 'ITC.NS':0.2,
    # 'IRCTC.NS':0.2,
    # 'IEX.NS':0.2,
    # 'NGLFINE.NS': 0.2,
#     'NEOGEN.NS': 0.2
}
weights_list=np.array(list(weights.values()))


# In[3]:


index = '^NSEI'

basket=list(weights.keys())
df= GetHistData_yf([index],start_time)
basketdf= GetHistData_yf(basket,start_time)


# In[4]:


# Calculate Index returns
df['daily_returns']=df['Adj Close'].pct_change()
df['cust_index']=(1+df['daily_returns']).cumprod()
df['cust_index'].plot(figsize=(16,4))


# In[5]:


tick_df=pd.DataFrame()
for i,tick in enumerate(basketdf['Symbol'].unique()):
    df1=basketdf.loc[basketdf['Symbol']==tick ,['Adj Close']]
    df1.rename(columns = {'Adj Close':tick}, inplace = True)
    if i==0 :
        tick_df=df1
    else:
        tick_df=pd.merge(tick_df,df1,left_index=True,right_index=True)

tick_df=tick_df.pct_change()


# In[6]:


if 'Portfolio' in tick_df.columns:
    del tick_df['Portfolio']
avgDailyReturns=np.sum(tick_df.mean()*weights_list)
avgDailyReturns

tick_df['Portfolio']=tick_df.dot(weights_list)


# In[7]:


daily_cum_ret=(1+tick_df).cumprod()


# In[8]:


daily_cum_ret.Portfolio.plot(figsize=(16,4))


# In[9]:


df['cust_index'].plot(figsize=(16,4))
(daily_cum_ret.Portfolio).plot()

benchmark_index=go.Scatter(x=df.index,y=df['cust_index'],name=index, line={'color':'black'})
basket_index=go.Scatter(x=daily_cum_ret.index,y=daily_cum_ret['Portfolio'],name='basket', line={'color':'red'})

fig = go.Figure(data=[basket_index, benchmark_index])
fig.update_layout(title='Basket stocks vs. {}'.format(index))
# fig.layout.xaxis.type='category'
fig.update_layout(
    autosize=False,
    width=1000,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    )
)
fig.show()


# In[13]:


bench_val=df['cust_index'][-1]
port_val=daily_cum_ret['Portfolio'][-1]

if df['cust_index'][-1] < daily_cum_ret['Portfolio'][-1] :
    print('your portfolio has outperformed {} by {}%'.format(index,round(((port_val/bench_val)-1),3)*100))
else:
    print('your portfolio has underperformed {} by {}%'.format(index,round(((port_val/bench_val)-1),3)*100))

