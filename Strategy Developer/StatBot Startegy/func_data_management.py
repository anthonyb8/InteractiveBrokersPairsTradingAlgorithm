#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 15:53:51 2022

@author: anthony

Data Manager
"""
from config_ws_connect import app
from func_handle_json import store_price_history, open_price_history
from func_ticker_contract import usStk
from config_strategy import timeframe, exchange, duration
import pandas_market_calendars as mcal
import os
from config_strategy import file_name
import time
from datetime import datetime, time, date


#retrieves the historical data in ticker by ticker loop, saved in the TradeApp
def fetchHistorical(duration, ticker):
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

def data_manager():
    PATH = '/Users/anthony/python/IB_trading/StatBot/DataFiles/' + file_name
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        app.hist_dict = open_price_history()
        update_hist_data()
    else:
        for ticker in app.shortable_tickers:
            fetchHistorical(duration, ticker)
            while app.ticker_done == False:
                continue
    #save to data json after being updated      
    store_price_history()

def update_hist_data():
        #current time
        current_time = datetime.now()
            
        #use first ticker to check date intervals in the dict
        first_ticker = next(iter(app.hist_dict))
        
        #set todays date the oldest date in the dictionary and the newest date in the dictionary
        today = date.today()              
        newest_date = datetime.strptime((app.hist_dict[first_ticker]['Date'])[len(app.hist_dict[first_ticker])-1], '%Y%m%d').date() #remove date for hourly data )
        oldest_date =  datetime.strptime((app.hist_dict[first_ticker]['Date'])[0],'%Y%m%d').date() #remove date for hourly data )
        
        if today == newest_date and datetime.time(current_time) < time(16,00,00):
            return
        else: 
            # Create a calendar
            ex_calendar = mcal.get_calendar(exchange)
            
            for ticker in app.shortable_tickers:
                print(ticker, app.shortable_tickers)#delete
        
                if ticker in app.shortable_tickers:
                    if ticker in app.hist_dict.keys():
                        duration = str(len(ex_calendar.schedule(newest_date, today))-1) +' D'
                        print(duration)
                        fetchHistorical(duration, ticker)
                    else:
                        duration = str(len(ex_calendar.schedule(oldest_date, today))) +' D'
                        print(duration)
                        fetchHistorical(duration, ticker)
                elif ticker in app.hist_dict.keys():
                    app.hist_dict.pop(ticker, None)
                
                #safety net to stop any duplicates from being added always keep second incase there is a diffference in time
                app.hist_dict[ticker].drop_duplicates(subset = ['Date'], keep ='last', inplace =  True, ignore_index = True)
                

data_manager() 
    
