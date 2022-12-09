#!/usr/bin/env python
# coding: utf-8


from nsepy import get_history
from datetime import datetime,timedelta
import yfinance as yf
import talib as tb
import pandas as pd
import time
from get_histdata import GetHistData_yf




def buy(df_in,tick,amount,start,end):
    """This function will calculate the returns you would have got if you had invested certain amount in this stock in the past.
    buy(tick,amount,start,end=None)
    returns 4 float values.
    -------------------------------        
    (df_in, pd.DataFrame)   = A pandas dataframe containing histrical prices.
                                Expected columns: 'Close', 'Symbol'
    (tick, str)             = The ticker symbol for the stock in listed stock exchange. [This function uses yfinance]
    (amount, int)           = The amount you wish you had invested.
    (start, datetime)       = The day you wish you had invested [YYYY-MM-DD].
    (end, datetime)         = Exit date. default is current date [YYYY-MM-DD].
    This function will take care of stock spilits.
    -------------------------------
    returns: (No of shares), (Entry price [price of 1 share at entry]),(Exit price [price of 1 share at exit]), (Current value), (Percentage increase/decrease)
    """
    from_date=datetime.strptime(start,'%Y-%m-%d')
    to_date=datetime.strptime(end,'%Y-%m-%d')

#   Get historic data for ticker provided
    security=yf.Ticker(tick)
    data=df_in.loc[start:end]
    
    entry_price=data['Close'].iloc[0]
    exit_price=data['Close'].iloc[-1]
    no_of_shares=round(amount/entry_price,3)
    # Calculate stock splits if any
    stock_splits=security.splits[from_date:to_date]
    for split in stock_splits:
        no_of_shares*=split
    curr_val=round(no_of_shares*exit_price,2)
    percentage=round((curr_val-amount)/amount*100,2)
    
    return no_of_shares,entry_price,exit_price,curr_val,percentage


def CalculateReturns(df_in,amount=10000,start=None,end=None):
    """This function will calculate the returns you would have got if you had invested certain amount in this stock in the past.
    CalculateReturns(df_in,amount=10000,start=None,end=None)
    >Returns a DataFrame
    -------------------------------        
    (df_in, pd.DataFrame)   = A pandas dataframe containing histrical prices.
                                Expected columns: 'Close', 'Symbol'
    (amount, int)           = The amount you wish you had invested.
    (start, str)       = The day you wish you had invested [YYYY-MM-DD]. Default is 90 days ago.
    (end, str)         = Exit date. default is current date [YYYY-MM-DD]. Default is current day.
    This function will take care of stock spilits.
    -------------------------------
    returns: a pandas DataFrame with columns:
    (Symbol  Shares  Entry_date   Exit_date  Entry_price  Exit_price  Invested  Current_val Days_HODL   Percentage_chg)
    """

    # Convert start and end (if provided) to datetime format
    if start==None:
        from_date=df_in.index[0].strftime('%Y-%m-%d')
    elif type(start) == str:
        from_date=start
    else:
        from_date=start.strftime("%Y-%m-%d")    
    
    if end==None:
        to_date=datetime.today().strftime("%Y-%m-%d")
    elif type(end) == str:
        to_date=end
    else:
        to_date=end.strftime("%Y-%m-%d") 
    # Convert index to datetimeIndex
    df_in.index=pd.to_datetime(df_in.index)

    from_date_i=datetime.strptime(from_date,'%Y-%m-%d')
    to_date_i=datetime.strptime(to_date,'%Y-%m-%d')

    start_time = time.time()
    tickers=df_in['Symbol'].unique()
    for i,tick in enumerate(tickers):
        cust_df=df_in[df_in['Symbol']==tick]
        shares,entry_price,exit_price,curr_val,percentage=buy(cust_df,tick,amount,from_date,to_date)
        
        dict_returns={'Symbol':tick, 'Shares':round(shares,1),'Entry_date':from_date, 'Exit_date':to_date, 
                    'Entry_price':round(entry_price,2),'Exit_price':round(exit_price,2),'Invested':amount, 
                    'Current_val':curr_val,'Days_HODL':abs((to_date_i - from_date_i).days), 'Percentage_chg':"{}%".format(percentage)}
        if i == 0 :
            returns_df=pd.DataFrame(dict_returns,index=[i])
        else :
            df2=pd.DataFrame(dict_returns,index=[i])
            returns_df=pd.concat([returns_df,df2])

    print("--- %s seconds ---" % (time.time() - start_time))
    return returns_df

def CalculateReturnsList(tickers,amount=10000,start=None,end=None):
    """This function will calculate the returns you would have got if you had invested certain amount in this stock in the past.
    CalculateReturnsList(tickers,amount=10000,start=None,end=None)
    returns a dataframe
    -------------------------------        
    (tickers, list)         = A List containg ticker symbols as listed in yfinance.
    (amount, int)           = The amount you wish you had invested.
    (start, str)       = The day you wish you had invested [YYYY-MM-DD].
    (end, str)         = Exit date. default is current date [YYYY-MM-DD].
    This function will take care of stock spilits.
    -------------------------------
    returns: a pandas DataFrame with columns:
    (Symbol  Shares  Entry_date   Exit_date  Entry_price  Exit_price  Invested  Current_val Days_HODL   Percentage_chg)
    """

    # Convert start and end (if provided) to datetime format
    if start==None:
        from_date=(datetime.today()-timedelta(90)).strftime("%Y-%m-%d")
    elif type(start) == str:
        from_date=start
    else:
        from_date=start.strftime("%Y-%m-%d")    
    
    if end==None:
        to_date=datetime.today().strftime("%Y-%m-%d")
    elif type(end) == str:
        to_date=end
    else:
        to_date=end.strftime("%Y-%m-%d") 

    from_date_i=datetime.strptime(from_date,'%Y-%m-%d')
    to_date_i=datetime.strptime(to_date,'%Y-%m-%d')

    start_time = time.time()
    for i,tick in enumerate(tickers):
        # ==================
    #   Get historic data for ticker provided
        security=yf.Ticker(tick)
        data= GetHistData_yf([tick],start,end)   
        entry_price=data['Close'].iloc[0]
        exit_price=data['Close'].iloc[-1]
        no_of_shares=round(amount/entry_price,3)
        # Calculate stock splits if any
        stock_splits=security.splits[from_date_i:to_date_i]
        for split in stock_splits:
            no_of_shares*=split
        curr_val=round(no_of_shares*exit_price,2)
        percentage=round((curr_val-amount)/amount*100,2)

        # ====================
        dict_returns={'Symbol':tick, 'Shares':round(no_of_shares,1),'Entry_date':from_date, 'Exit_date':to_date, 
                    'Entry_price':round(entry_price,2),'Exit_price':round(exit_price,2),'Invested':amount, 
                    'Current_val':curr_val,'Days_HODL':abs((to_date_i - from_date_i).days), 'Percentage_chg':"{}%".format(percentage)}
        if i == 0 :
            returns_df=pd.DataFrame(dict_returns,index=[i])
        else :
            df2=pd.DataFrame(dict_returns,index=[i])
            returns_df=pd.concat([returns_df,df2])

    print("--- %s seconds ---" % (time.time() - start_time))
    return returns_df

def main():
    print("Call CalculateReturns function")
if __name__=='__main__':
    main()
