#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
import yfinance as yf
import pandas as pd
from get_histdata import GetHistData_yf
from getTickers import nifty50tickers
import seaborn as sns
import matplotlib.pyplot as plt # for data visualization


def monthlyreturnheatmap(ticker,start=None,end=None):
    '''This function will return a seaborn plot object which can be plotted with '.show()' method

    usage: monthlyreturnheatmap(ticker,start=None,end=None)

    returns a heatmap of monthly returns for the time period provided
    _____________________________________________________
    (ticker, str)   : Stock ticker as listed on yfinance.
    ex. ticker symbol for TCS is TCS.NS

    ex: monthlyreturnheatmap('TCS.NS','2018-01-01')
    
    '''
    tick=[]
    tick.append(ticker)
    df2= GetHistData_yf(tick,start,end)
    # df.head()
    if not df2.empty:
        df2.index=pd.to_datetime(df2.index)
    else:
        print("Unable to fetch data for {}".format(tick))
        return False

    def historic_data(df2):
        returns_df = pd.DataFrame(columns=['Symbol', 'Year', 'Month','Returns'])

        for symbol in df2['Symbol'].unique():
            data_tick=df2[df2['Symbol']==symbol]
            for year in data_tick.index.year.unique():
                dat_yr=data_tick[data_tick.index.year==year]

                for i in range(12):
                    dat_month=dat_yr[dat_yr.index.month==i+1]

                    if not dat_month.empty:
                        return_val=round(((dat_month['Close'][-1]-dat_month['Close'][0])/dat_month['Close'][0])*100,3)
                        dict_returns={'Symbol':dat_month['Symbol'][0], 'Year':year,'Month':i+1, 'Returns':return_val}
                        returns_df=pd.concat([returns_df,pd.DataFrame(dict_returns,index=[year])])
        return returns_df


    returns_df=historic_data(df2)


    df_1=returns_df[(returns_df['Symbol']==ticker)]
    df_2=df_1.drop(columns=['Symbol'],axis=1)



    df_ret=pd.pivot_table(df_2, values = 'Returns', index=['Month'], columns = 'Year')

    plt.figure(figsize=(18,9))
    plt.title(ticker, fontsize = 25)
    fig1=sns.heatmap(df_ret,cmap="magma",annot=True,center=0,robust=True)

    fig=fig1.get_figure()
    fig.savefig(f"{ticker}.png")

    return fig



