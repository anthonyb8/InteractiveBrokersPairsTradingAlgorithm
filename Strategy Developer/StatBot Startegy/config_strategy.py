"""
API Configuration:
- For a rest API for pybit

"""
#Configuration
account = 'U4976268'
mode = 'paper' #paper or live
timeframe = '1 Day' #time window examining
duration = '200 D' #maximum data size 200 days(specific to each api)
z_score_window = 21 #moving average window for z-score

#Live API
live_port_key = 7496 # port 4001 for ib gateway

#Paper API
paper_port_key = 7497 # port 4002 for ib gateway

#Selected API port
port_key = paper_port_key if mode =='paper' else live_port_key

#Daily time Frame
D_file_name = '2_Daily_Data.json'

#Hourly Time Frame
H_file_name = '2_Hourly_Data.json'

#Data File Name 
file_name = D_file_name if timeframe =='1 Day' else H_file_name

#tickers
exchange = 'NASDAQ'
ticker_file_name = '1_' + exchange +'_tickers.json'

#connects to fmp api and retrieves from inputed exchange
import requests
import pandas as pd

def retrieve_tickers():
    api_key = '517687b7075bb5d5115d85355e3dbd41'
    ticker_info = pd.DataFrame(requests.get(f'https://financialmodelingprep.com/api/v3/stock-screener?exchange='+ exchange +'&apikey=' + api_key).json())
    tickers = list(ticker_info['symbol'])
    return tickers

all_tickers = retrieve_tickers()