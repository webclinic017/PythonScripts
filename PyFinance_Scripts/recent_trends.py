
def recent_trends(df_in,uptrend_period=10):
    print("Printing continuous {} days uptrends.".format(uptrend_period))
    tickers=df_in['Symbol'].unique()
    for ticker in tickers:
        print(ticker)
        count=0
        up_trend=0
        data=df_in[df_in['Symbol']==ticker]
        for i,close in enumerate(data['Close']):
            # On finding a GREEN candle
            if data['Close'][i]>data['Open'][i]:
                if count == 0:
                    start_1=data['Open'].index[i]
                end_1=data['Close'].index[i]
                count+=1  
            # On finding a RED candle
            # If the close is still higher than yesterday's average
            elif data['Close'][i]>(data['Close'][i-1]+data['Open'][i-1])/2:
                continue;
            else:
                if count<uptrend_period:
                    count=0
                else:
                    up_trend+=1
                    end_1=data['Close'].index[i-1]
                    count=0
                    if data.loc[start_1,'Close'] >= data.loc[end_1,'Close']:
                        continue
                    # Calculate % increase during this uptrend
                    
                    chg_p=(data.loc[end_1,'Close']-data.loc[start_1,'Close'])/data.loc[start_1,'Close']*100
                    print("from {} to {} : {}% [{} --> {}]".format(start_1,end_1,round(chg_p,2),round(data.loc[start_1,'Close'],2),round(data.loc[end_1,'Close'],2)))
        if data.loc[start_1,'Open'] >= data.loc[end_1,'Close']:
            print("====================")
            continue
        print("Most recent observed trend...")
        chg_p=(data.loc[end_1,'Close']-data.loc[start_1,'Open'])/data.loc[start_1,'Open']*100
        print("from {} to {} : {}% [{} --> {}]".format(start_1,end_1,round(chg_p,2),round(data.loc[start_1,'Open'],2),round(data.loc[end_1,'Close'],2)))
        print("====================")
