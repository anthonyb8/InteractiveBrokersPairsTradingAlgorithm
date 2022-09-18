# Import libraries
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from func_ticker_contract import usStk
from config_strategy import all_tickers, timeframe, exchange, duration
import threading
import pandas as pd
from datetime import date, datetime, timedelta
import pandas_market_calendars as mcal

ticker_event = threading.Event()#cycle through tickers to get historical data

#contains all the IB wrapper functions
class TradeApp(EWrapper, EClient): 
    def __init__(self): 
        EClient.__init__(self, self) 
        self.hist_dict =  {}
        self.shortable_tickers = []
        self.ticker_done = None
    
#####   wrapper function for reqHistoricalData. this function gives the candle historical data
    def historicalData(self, reqId, bar):
        self.ticker_done = False
        if self.shortable_tickers[reqId] not in self.hist_dict:
            self.hist_dict[self.shortable_tickers[reqId]] = pd.DataFrame([{"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}])#.set_index('Date')
        else:
            df = pd.DataFrame([{"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}])#.set_index('Date')
            self.hist_dict[self.shortable_tickers[reqId]] = pd.concat([self.hist_dict[self.shortable_tickers[reqId]],df], axis=0, ignore_index=True)
 
#####   wrapper function for reqHistoricalData. this function triggers when historical data extraction is completed      
    def historicalDataEnd(self, reqId, start, end):       
        print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
        self.ticker_done = True
        ticker_event.set()  
            
##### wrapper function for reqMktData. this function handles streaming market data    
    def tickGeneric(self, reqId, tickType, value):
        super().tickGeneric(reqId, tickType, value)
        if all_tickers[reqId] in self.shortable_tickers:
            self.cancelMktData(reqId)
        else:
            if tickType == 46 and value > 1.5:
                self.shortable_tickers.append(all_tickers[reqId])
                self.cancelMktData(reqId)
        
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
    for ticker in app.shortable_tickers:
        ticker_event.clear()
        app.reqHistoricalData(reqId=app.shortable_tickers.index(ticker), 
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
"""
#retrieves the historical data in ticker by ticker loop, saved in the TradeApp
def fetchHistorical(duration, ticker, tickers):
    app.reqHistoricalData(reqId=app.shortable_tickers.index(ticker), 
                          contract=usStk(ticker),
                          endDateTime='',
                          durationStr= duration,
                          barSizeSetting=  timeframe,
                          whatToShow='ADJUSTED_LAST',
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=0,
                          chartOptions=[])	 # EClient function to request contract details

def update_hist_data(tickers):
    
    if len(app.hist_dict) > 0:
            
        #use first ticker to check date intervals in the dict
        first_ticker = next(iter(app.hist_dict))
        
        #set todays date the oldest date in the dictionary and the newest date in the dictionary
        today = date.today()              
        newest_date = datetime.strptime((app.hist_dict[first_ticker]['Date'])[len(app.hist_dict[first_ticker])-1], '%Y%m%d').date() #remove date for hourly data )
        oldest_date =  datetime.strptime((app.hist_dict[first_ticker]['Date'])[0],'%Y%m%d').date() #remove date for hourly data )
        
        # Create a calendar
        ex_calendar = mcal.get_calendar(exchange)
        
        #check if tickers in the shortabel list are in the dict and update
        #if not in shortable list but dict delete
        for ticker in  tickers:
            ticker_event.clear()
            print(ticker, tickers)#delete
    
            if ticker in app.shortable_tickers:
                if ticker in app.hist_dict.keys():
                    duration = str(len(ex_calendar.schedule(newest_date, today))-1) +' D'
                    print(duration)
                    fetchHistorical(duration, ticker, tickers)
                else:
                    duration = str(len(ex_calendar.schedule(oldest_date, today))) +' D'
                    print(duration)
                    fetchHistorical(duration, ticker, tickers)
            elif ticker in app.hist_dict.keys():
                app.hist_dict.pop(ticker, None)
                
            ticker_event.wait()
    

#handling if the file is empty/ doesnt exist
#writing into json so that it over writes and doesnt append
#not having data for today if today isnt over
"""
