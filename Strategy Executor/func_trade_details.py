from config_execution_api import stop_loss_fail_safe
from config_execution_api import pos_ticker
#from config_execution_api import rounding_ticker_1
#from config_execution_api import rounding_ticker_2
#from config_execution_api import quantity_rounding_ticker_1
#from config_execution_api import quantity_rounding_ticker_2


# Get trade details and latest prices
def get_trade_details(ticker, ask_prices, bid_prices, direction="Long", capital=0):
    # Set calculation and output variables
    #price_rounding = rounding_ticker_1 if ticker == pos_ticker else rounding_ticker_2
    #quantity_rounding = quantity_rounding_ticker_1 if ticker == pos_ticker else quantity_rounding_ticker_2
    mid_price = 0
    quantity = 0
    stop_loss = 0

    # Calculate price, size, stop loss and average liquidity
    if len(ask_prices) > 0 and len(bid_prices) > 0:
        # Get nearest ask, nearest bid and orderbook spread
        nearest_ask = ask_prices[ticker]
        nearest_bid = bid_prices[ticker]
        
        # Calculate hard stop loss
        if direction == "Long":
            mid_price = nearest_bid # placing at Bid has high probability of not being cancelled, but may not fill
            stop_loss = round(mid_price * (1 - stop_loss_fail_safe), 2)
        else:
            mid_price = nearest_ask  # placing at Ask has high probability of not being cancelled, but may not fill
            stop_loss = round(mid_price * (1 + stop_loss_fail_safe), 2)
        # Calculate quantity
        quantity = round(capital / mid_price, 0)

    # Output results
    return (mid_price, stop_loss, quantity)

