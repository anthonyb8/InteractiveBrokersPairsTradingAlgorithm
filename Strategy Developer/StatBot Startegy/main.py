
from config_ws_connect import app
from config_ws_connect import fetchHistorical#, update_hist_data
from func_get_symbols import get_tradeable_symbols
from func_handle_json import store_price_history, open_price_history, store_tickers, open_tickers
from func_cointegration import get_cointegrated_pairs
from func_plot_trends import plot_trends
import pandas as pd

"""STRATEGY CODE"""
if __name__ == "__main__":   
    
    # #STEP 1 - Get list of symbols
    #print("Getting symbols...")
    #signal = get_tradeable_symbols()
    #if signal:
    #    store_tickers()
    
    # # STEP 2 - Construct and save price history
    print("Constructing and saving price data to JSON...")
    app.shortable_tickers = open_tickers()
    app.shortable_tickers = app.shortable_tickers[:20] #delete
    fetchHistorical()
    store_price_history()
    
    
    # # # STRATEGY SPECIFIC
    # # STEP 3 - Find Cointegrated pairs
    print("Calculating co-integration...")
    app.hist_dict = open_price_history()
    if len(app.hist_dict) > 0:
        coint_pairs = get_cointegrated_pairs(app.hist_dict)
    print('Done')
    
    
    # # STEP 4 - Plot trends and save for backtesting
    print("Plotting trends...")
    coint_pairs_df = pd.read_csv('3_cointegrated_pairs.csv') 

    symbol_1 = coint_pairs_df['sym_1'][1]
    symbol_2 = coint_pairs_df['sym_2'][1]
    price_data = open_price_history()
    if len(price_data) > 0:
        plot_trends(symbol_1, symbol_2, price_data)


