from config_execution_api import tickers, timeframe, duration
from func_ticker_contract import usStk
from config_ws_connect import app

####  this function starts the streaming data of current ticker.
def streamSnapshotData(ticker):
    """stream tick leve data"""
    app.reqMktData(reqId=tickers.index(ticker), 
                   contract=usStk(ticker),
                   genericTickList="",
                   snapshot=False,
                   regulatorySnapshot=False,
                   mktDataOptions=[])
    
#retrieves the historical data in ticker by ticker loop, saved in the TradeApp
def fetchHistorical(ticker):
    app.reqHistoricalData(reqId=tickers.index(ticker), 
                          contract=usStk(ticker),
                          endDateTime='',
                          durationStr= duration,
                          barSizeSetting= timeframe,
                          whatToShow='ADJUSTED_LAST',
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=0,
                          chartOptions=[])	 # EClient function to request contract details
    
#Cycles through tickers to get all historical data before moving on
def historical_data():
    for ticker in tickers:
        fetchHistorical(ticker)
        while app.data_event != True:
            continue
        
#Cycles through tickers to get all historical data before moving on
def live_data():
    for ticker in tickers:
        streamSnapshotData(ticker)
