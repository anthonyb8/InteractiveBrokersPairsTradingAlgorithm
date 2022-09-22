"""
    API Documentation
    https://interactivebrokers.github.io/tws-api/introduction.html
    
"""
# # CONFIG VARIABLES
account = 'U4976268' #INSERT IB ACCOUNT
mode = 'paper' #paper or live
limit_order_basis = False # will ensure orders opend with limit order
stop_loss_fail_safe = 0.15 # stop loss at market order in case of drastic event
#tradeable_capital_usdt = 500 # total tradeable capital to be split between both pairs

# # From Back-test Strategy
tickers = ["MA" ,"VZ"]
pos_ticker = tickers[0]
neg_ticker = tickers[1]
tickers = [pos_ticker, neg_ticker]
signal_trigger_thresh = 1.1 # z-score threshold
timeframe = '1 hour' #timeframe
duration = '365 D' #max duration allowed by IB API
z_score_window = 21 # make sure matches your strategy

""" # From IB API
rounding_ticker_1 = 2 #FOR LATER: check the IB API for data values
rounding_ticker_2 = 2
quantity_rounding_ticker_1 = 0
quantity_rounding_ticker_2 = 0
"""

#Selected API port
live_port_key = 7496 # port 4001 for ib gateway
paper_port_key = 7497 # port 4002 for ib gateway
port_key = paper_port_key if mode =='paper' else live_port_key

#Execution Parameters
strategy_capital_percent = 0.5
