import quantstats as qs
qs.extend_pandas()

stock = qs.utils.download_returns('IEX.NS')

# qs.reports.html(stock,"^NSEI",title='NIFTY vs IEX', output='IEX_vs_NIFTY.html')

weights={
'CHAMBLFERT.NS' : 0.036,
'FINPIPE.NS' : 0.06,
'INFY.NS' : 0.03,
'JKLAKSHMI.NS' : 0.018,
'JUNIORBEES.NS' : 0.024,
'KIRLFER.NS' : 0.048,
'LT.NS' : 0.024,
'NIFTYBEES.NS' : 0.25,
'ORIENTCEM.NS' : 0.065,
'POLYPLEX.NS' : 0.006,
'REDINGTON.NS' : 0.077,
'SBIN.NS' : 0.042,
'SHK.NS' : 0.065,
'TATAMOTORS.NS' : 0.042,
'TATAPOWER.NS' : 0.149,
'TCS.NS' : 0.03,
'WIPRO.NS' : 0.036,
}

portfolio=qs.utils.make_index(weights,period="5Y")

# qs.reports.html(portfolio,"^NSEI",output='MyPortfolio.html')
print(portfolio)