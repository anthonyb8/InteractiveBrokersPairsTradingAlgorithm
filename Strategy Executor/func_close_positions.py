from config_ws_connect import app
from config_execution_api import tickers, neg_ticker, pos_ticker
from func_execution_calls import marketOrder
from func_ticker_contract import usStk
from func_position_calls import get_open_positions
import time

#Only works for orders submitted through API
def cancel_active_order(ticker):
    app.reqOpenOrders()#Get active orders from api
    #cancel orders for specific tickers
    if ticker in app.order_dict.keys():
        app.cancelOrder(app.order_dict[ticker]['OrderId'])
        print(' Order Cancelled for: ', ticker)

# Close all positions for both tickers
def close_all_positions():
    
    #cancel open orders realetd to strategy
    cancel_active_order(neg_ticker)
    cancel_active_order(pos_ticker)
    #app.reqGlobalCancel() #cancels all open orders incuding manual orders

    #get position information
    _,size_P, side_P = get_open_positions(pos_ticker)
    _,size_N,side_N = get_open_positions(neg_ticker)

    #close positions
    app.reqIds(-1)#eclient function for next valid ID
    time.sleep(1)
    for ticker in tickers:
        quantity = app.pos_dict[ticker]['Quantity']
        if quantity > 0:
            app.placeOrder(app.nextValidOrderId,usStk(ticker),marketOrder("SELL",quantity)) # EClient function to request contract details
        if quantity < 0:
            app.placeOrder(app.nextValidOrderId,usStk(ticker),marketOrder("BUY",abs(quantity))) 
        app.nextValidOrderId+=1
        
    print(" Positions Closed")
    
    trade_progress = 0 
    return trade_progress




"""
# Get position information
def get_position_info1(ticker):
    # Declare output variables
    side = ''
    size = 0
    
    if ticker in app.pos_dict.keys():
            if app.pos_dict[ticker]['Quantity'] > 0:
                side = 'BUY'
                size = app.pos_dict[ticker]['Quantity']
            elif app.pos_dict[ticker]['Quantity'] < 0:
                side = 'SELL'
                size = abs(app.pos_dict[ticker]['Quantity'])
                
    # Return output
    return side, size
"""

