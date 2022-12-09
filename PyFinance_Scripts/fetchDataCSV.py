import os
import pandas as pd
from get_histdata import GetHistData_yf
from getTickers import nifty200tickers,nifty50tickers
import plotly.graph_objects as go
from datetime import datetime,timedelta
import warnings
warnings.simplefilter(action='ignore', category=Warning)

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
def check_csv(data_file):
    '''Checks if the data_file provided exists and if it is latest
    Returns a Boolean
    ___________________
    (data_file, str(path))      : Full path or relative path of the file.
    '''

    if os.path.exists(data_file) and (datetime.today().strftime('%Y-%m-%d')==datetime.strftime(datetime.fromtimestamp(os.path.getmtime(data_file)),'%Y-%m-%d')):
        return True
    else:
        return False


def fetchDataCSV(tickers,data_file,from_date=None,to_date=None):

    if not check_csv(data_file):
        df = GetHistData_yf(tickers,from_date,to_date)
        df.to_csv("{}".format(data_file))

    df=pd.read_csv(data_file,index_col='Date')
    df.index=pd.to_datetime(df.index)
    df['Close']=df['Adj Close']
    df.drop(columns='Adj Close',inplace=True)

    return df

