
from datetime import datetime
import yfinance as yf
import pandas as pd
from get_histdata import GetHistData_yf
from getTickers import nifty50tickers

tickers=nifty50tickers()
tickers=["{}.NS".format(tick) for tick in tickers]
# print(tickers)
df= GetHistData_yf(tickers)
print(df.tail())