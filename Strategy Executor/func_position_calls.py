from config_ws_connect import app
from config_execution_api import tickers
import time

# Get position information
def check_open_positions(ticker):
    if ticker in app.pos_dict.keys():
        return True
    else:
        return 

# Get open position price and quantity
def get_open_positions(ticker):
    if check_open_positions(ticker) == True: #test if there is a position
            if app.pos_dict[ticker]['Quantity'] > 0:
                side = 'BUY'
                size = app.pos_dict[ticker]['Quantity']
                price = app.pos_dict[ticker]['AverageCost']
            elif app.pos_dict[ticker]['Quantity'] < 0:
                side = 'SELL'
                size = abs(app.pos_dict[ticker]['Quantity'])
                price = app.pos_dict[ticker]['AverageCost']
                
            return price, size, side
    else:
        return

# Check for active orders
def check_open_orders(ticker):
    if ticker in app.order_dict.keys():
        return True
    else:
        return 
        
        
# Get active orders price and quantity
def get_open_orders(ticker):
    if check_open_orders(ticker) == True:
        size = app.order_dict[ticker]['Quantity']
        price = app.order_dict[ticker]['LmtPrice']
        side = app.order_dict[ticker]['Action']
        return price, size, side
    
    else:
        return
    
def orders_positions():
    #Get current positions/orders
    app.reqPositions()
    app.reqOpenOrders()
    
    check = []
    for ticker in tickers:
        check.append(check_open_positions(ticker))
        check.append(check_open_orders(ticker))
    
    return check

def confirm_order_executed(long_quantity, short_quantity, long_ticker, short_ticker):
    app.reqOpenOrders()
    time.sleep(3)
    
    while len(app.order_dict) > 0:
        app.reqOpenOrders()
        time.sleep(3)
    
    #get postions
    app.reqPositions()
    
    #Check that positions were comletely filled
    if app.pos_dict[long_ticker]['Quantity'] == long_quantity and app.pos_dict[short_ticker]['Quantity'] == short_quantity:
        return True
    else:
        print('Warning: One or both positions were not completely filled ')
        return False

        
    