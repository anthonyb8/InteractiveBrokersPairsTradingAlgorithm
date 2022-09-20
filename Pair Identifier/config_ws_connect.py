
# Import libraries
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from func_ticker_contract import usStk
from config_strategy import all_tickers, timeframe, duration
import threading
import pandas as pd

ticker_event = threading.Event()

#contains all the Interactive Brokers wrapper functions
class TradeApp(EWrapper, EClient): 
    def __init__(self): 
        EClient.__init__(self, self) 
        self.hist_dict =  {}
        self.tickers = all_tickers
        self.data_done = None
    
#####   wrapper function for reqHistoricalData. this function gives the candle historical data
    def historicalData(self, reqId, bar):
        self.data_done = False
        if self.tickers[reqId] not in self.hist_dict:
            self.hist_dict[self.tickers[reqId]] = pd.DataFrame([{"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}])#.set_index('Date')
        else:
            df = pd.DataFrame([{"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}])#.set_index('Date')
            self.hist_dict[self.tickers[reqId]] = pd.concat([self.hist_dict[self.tickers[reqId]],df], axis=0, ignore_index=True)
 
#####   wrapper function for reqHistoricalData. this function triggers when historical data extraction is completed      
    def historicalDataEnd(self, reqId, start, end):       
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
        ticker_event.set()  
        
#establish the deamon thread that holds the api connection 
def API_connection():   
    app = TradeApp()
    app.connect(host='127.0.0.1', port=7497, clientId=23) #port 4002 for ib gateway paper trading/7497 for TWS paper trading
    con_thread = threading.Thread(target=app.run, daemon=True)
    con_thread.start()
    while app.isConnected() == False:
        print('Waiting for Connection')	
        continue
    
    print('Established Connection')	
    return app

app = API_connection()


#retrieves the historical data in ticker by ticker loop, saved in the TradeApp
def fetchHistorical():
    app.tickers = all_tickers
    for ticker in app.tickers:
        ticker_event.clear()
        app.reqHistoricalData(reqId=app.tickers.index(ticker), 
                              contract=usStk(ticker),
                              endDateTime='',
                              durationStr= duration,
                              barSizeSetting=  timeframe,
                              whatToShow='ADJUSTED_LAST',
                              useRTH=1,
                              formatDate=1,
                              keepUpToDate=0,
                              chartOptions=[])	 # EClient function to request contract details
        ticker_event.wait()
    app.data_done = True
    