to get historical data :

    from yfinance   
        import yfinance as yf
        from get_histdata import GetHistData_yf()
        hist_df=GetHistData_yf(df_in)

    from nsepy    
        from nsepy as get_history
        from get_histdata import GetHistData_nse()
        hist_df=GetHistData_nse(df_in)   

to find consolidating/breakingout stocks-

    from scan_breakouts import daily_scan
    daily_scan(df_in,period=10,pct_chg=2.5)

to regret and cry

    from regret_calc import CalculateReturns
    CalculateReturns(df_in,amount=10000,start=None,end=None)

to get list of ticker symbols 
    from getTickers import nifty50tickers,nifty200tickers

    call them with out any args; list is returned.

to get each heatmap of each month returns of a stock
    from eachmonthret import monthlyreturnheatmap
    monthlyreturnheatmap('TCS.NS','2018-01-01').show()

    