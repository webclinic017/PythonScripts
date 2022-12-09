import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime,timedelta
import time
from get_histdata import GetHistData_yf
from regret_calc import CalculateReturns
from recent_trends import recent_trends


# Variables for yfinance
look_back=45 #days ago
look_upto=0 #days ago; 0=today
uptrend_period=90 #days
interval='1d'

to_date=(datetime.today()-timedelta(look_upto)).strftime("%Y-%m-%d")
from_date=(datetime.today()-timedelta(look_back)).strftime("%Y-%m-%d")
# Convert string datetime to datetime datatype
to_date=datetime.strptime(to_date,"%Y-%m-%d")
from_date=datetime.strptime(from_date,"%Y-%m-%d")


data=pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')[1]
tickers_nse=data['Symbol'].to_list()
tickers_yf=["{}.NS".format(tick) for tick in tickers_nse]

df=GetHistData_yf(tickers_yf)
print(CalculateReturns(df))
print(recent_trends(df))