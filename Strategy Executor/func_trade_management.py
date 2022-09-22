from config_execution_api import pos_ticker, neg_ticker, tickers, strategy_capital_percent, account, signal_trigger_thresh, limit_order_basis
from config_ws_connect import app
from func_get_zscore import get_latest_zscore
from func_execution_calls import initialise_order_execution
from func_close_positions import close_all_positions
from func_position_calls import confirm_order_executed
from func_price_calls import live_data
import time


def position_manager(signal_sign_positive):
    #get updated account info
    app.data_event == False
    app.reqAccountUpdates(True, account)
    time.sleep(3)
    while not app.data_event:
        continue
    
    #get strategy capital
    cash_balance = float(app.account_dict['CashBalance'])
    strategy_captial = cash_balance * strategy_capital_percent
    
    #equal capital on both sides of the trade
    capital_long = strategy_captial * 0.5
    capital_short = strategy_captial - capital_long
    
    # Determine long ticker vs short ticker
    if signal_sign_positive:
        long_ticker = pos_ticker
        short_ticker = neg_ticker
    else:
        long_ticker = neg_ticker
        short_ticker = pos_ticker
    
    return long_ticker, short_ticker, capital_long, capital_short

# Manage new trade assessment and order placing
def manage_new_trades(trade_progress):

    # Signal Variables
    signal = False
    signal_side = ""
    long_order = False 
    short_order = False

    # Get and save the latest z-score
    zscore, signal_sign_positive = get_latest_zscore()
    
    # Switch to hot if meets signal threshold
    # Note: You can add in coint-flag check too if you want extra vigilence
    if abs(zscore) > signal_trigger_thresh:

        # Active hot trigger
        signal = True
        print("-- Trade Status HOT --")
        print("-- Placing and Monitoring Existing Trades --")
        
        # Update signal side
        signal_side = "postive" if zscore > 0 else "negative"
    
    #signal is true and there is no current trade in process
    if signal and trade_progress == 0:
        long_ticker, short_ticker, long_capital, short_capital  = position_manager(signal_sign_positive)
        
        print(long_ticker,long_capital,  short_ticker, short_capital)

        #while trade_progress == 0:
        live_data()

        # Place order - long
        if long_order == False:
            long_quantity = initialise_order_execution(long_ticker, "Long", long_capital)
            long_order = True if long_quantity else False

        # Place order - short
        if short_order == False and long_order == True:
            short_quantity = initialise_order_execution(short_ticker, "Short", short_capital)
            short_order = True if short_quantity else False

        #No need to check on market orders
        if not limit_order_basis and long_order and short_order:
            trade_progress = 1
            #break

        # Check on Limit orders
        # Check limit orders and ensure z_score is still within range
        zscore_new, signal_sign_positive_new = get_latest_zscore() ###runaway loop
        
        if trade_progress == 0:
            print('Checking Orders')
            #if abs(zscore_new) > signal_trigger_thresh * 0.9 and signal_sign_positive_new == signal_sign_positive:
                        
            # Check long order status
            if long_order == True and short_order == True:
                completed_orders = confirm_order_executed(long_quantity, short_quantity, long_ticker, short_ticker)
                
                if completed_orders:
                    trade_progress = 1 
                    long_order = False
                    short_order = False
                else:
                    #balance out the orders
                    long_order = True
                    short_order = True

            """else:
                # Cancel all active orders
                trade_progress = close_all_positions()"""

    # Output status
    return trade_progress, signal_side
