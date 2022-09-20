"""
API Configuration:
- For a rest API for pybit

"""
#Configuration
account = 'U4976268' 
mode = 'paper' #paper or live
timeframe = '1 Day' #time window examining
duration = '365 D' #maximum for Interactive Brokers
z_score_window = 21 #moving average window for z-score

#Live API
live_port_key = 7496 # port 4001 for ib gateway

#Paper API
paper_port_key = 7497 # port 4002 for ib gateway

#Selected API port
port_key = paper_port_key if mode =='paper' else live_port_key

#Daily time Frame
D_file_name = 'Daily_Data.json'

#Hourly Time Frame
H_file_name = 'Hourly_Data.json'

#Data File Name 
file_name = D_file_name if timeframe =='1 Day' else H_file_name

#tickers
all_tickers = [ 'AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOGL', 'UNH', 'JNJ', 'XOM', 
               'META','NVDA','JPM','PG','V','CVX','HD','MA','PFE','ABBV', 'KO', 'LLY', 'BAC',
               'PEP', 'COST', 'MRK', 'TMO', 'AVGO', 'DIS', 'MCD', 'WMT', 'CSCO', 'ACN', 'ABT',
               'DHR', 'ADBE', 'VZ', 'NEE', 'WFC', 'CMCSA','CRM', 'TXN', 'PM', 'BMY', 'UPS', 
               'QCOM', 'COP', 'UNP', 'LIN', 'NKE']