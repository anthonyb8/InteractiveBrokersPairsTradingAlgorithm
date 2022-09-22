from config_execution_api import limit_order_basis
from config_ws_connect import app 
from func_trade_details import get_trade_details
from ibapi.order import Order
from func_ticker_contract import usStk
import time

# Place limit close order
def limitOrder(direction, quantity, lmt_price):
    order = Order()
    order.action = direction #BUY/SELL
    order.orderType = 'LMT'
    order.totalQuantity = quantity #number of shares
    order.lmtPrice = lmt_price
    return order

#  Place market close order
def marketOrder(direction, quantity):
    order = Order()
    order.action = direction #BUY/SELL
    order.orderType = 'MKT'
    order.totalQuantity = quantity #number of shares
    return order

# Place limit or market order
def place_order(ticker, lmt_price, quantity, stop_loss, direction):
    # Set variables
    if direction == "Long":
        side = "BUY"
    else:
        side = "SELL"
    
    #get next valid ID
    app.reqIds(-1)
    time.sleep(2)
    # Place limit order ele market order
    if limit_order_basis:
        app.placeOrder(app.nextValidOrderId,usStk(ticker),limitOrder(side, quantity, lmt_price))
    else:
        app.placeOrder(app.nextValidOrderId,usStk(ticker), marketOrder(side, quantity)) 

# Initialise execution
def initialise_order_execution(ticker, direction, capital):
    
    if len(app.ask_price_dict) > 0 and len(app.bid_price_dict) > 0:
        mid_price, stop_loss, quantity = get_trade_details(ticker, app.ask_price_dict, app.bid_price_dict, direction, capital)
        print(ticker, mid_price, stop_loss, quantity )
        print('Ticker:', ticker, 'Dircetion:',direction, "Order Price: ", mid_price, "Stop Loss:", stop_loss, "Quantity: ", quantity )
        if quantity != 0:
            place_order(ticker, mid_price, quantity, stop_loss, direction)
            return quantity
        else:
            return 0
            