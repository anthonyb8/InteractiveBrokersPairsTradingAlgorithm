
from config_ws_connect import app
from config_ws_connect import fetchHistorical
from func_cointegration import get_cointegrated_pairs
from func_plot_trends import plot_trends

if __name__ == "__main__":   
    
    # # STEP 1 - Construct and save price history
    print("Retrieving price data...")
    fetchHistorical()
    
    # # STEP 2 - Find Cointegrated pairs
    print("Calculating co-integration...")
    if len(app.hist_dict) > 0:
        coint_pairs = get_cointegrated_pairs(app.hist_dict)
    print('Done')
    
    # # STEP 3 - Plot trends and save for backtesting
    print("Plotting trends...")
    symbol_1 = coint_pairs['sym_1'][0]
    symbol_2 = coint_pairs['sym_2'][0]
    if len(app.hist_dict) > 0:
        plot_trends(symbol_1, symbol_2, app.hist_dict)


