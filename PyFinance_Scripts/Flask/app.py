from flask import Flask,render_template, request
from patterns import pattern_dict
from get_histdata import GetHistData_yf
from getTickers import nifty50tickers,nifty200tickers
import pandas as pd
import talib as ta


app = Flask(__name__)

ticker=nifty50tickers()
ticker=["{}.NS".format(tick) for tick in ticker]

# df = GetHistData_yf(ticker)  
# df.to_csv('datasets/Nifty50.csv')
# df=pd.read_csv("datasets/Nifty50.csv")
# df.index=pd.to_datetime(df.index)

@app.route("/")
def index():
    pattern = request.args.get('Pattern',None)
    stocks={}
    if pattern:
        df=pd.read_csv("datasets/Nifty200.csv",index_col='Date')
        df.index=pd.to_datetime(df.index)

        pattern_func=getattr(ta,pattern)
        for tick in df['Symbol'].unique():
            stocks[tick]={'Symbol':tick}
            df1=df[df['Symbol']==tick]
            try:
                result=pattern_func(df1['Open'], df1['High'], df1['Low'], df1['Close'])
                last=result.tail(1).values[0]
                if last > 0:                        
                    stocks[tick][pattern]='bullish'
                elif last < 0:
                    stocks[tick][pattern]='bearish'
                else:
                    stocks[tick][pattern]=None
            except:
                pass

    return render_template('index.html',patterns=pattern_dict,stocks=stocks,current_pattern=pattern)


@app.route("/snapshot")
def snapshot():
    df = GetHistData_yf(ticker)  
    df.to_csv('datasets/Nifty200.csv')
    return  'Done'
