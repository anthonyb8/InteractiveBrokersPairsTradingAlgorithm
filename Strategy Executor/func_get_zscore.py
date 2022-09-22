from config_ws_connect import app
from config_execution_api import pos_ticker, neg_ticker, tickers 
from func_price_calls import fetchHistorical, live_data
from func_trade_details import get_trade_details
#from func_price_calls import get_hist_price
#from func_stats import calculate_metrics
from config_execution_api import z_score_window
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import pandas as pd


# Calculate Z-Score
def calculate_zscore(spread):
    df = pd.DataFrame(spread)
    mean = df.rolling(center=False, window=z_score_window).mean()
    std = df.rolling(center=False, window=z_score_window).std()
    x = df.rolling(center=False, window=1).mean()
    df["ZSCORE"] = (x - mean) / std
    return df["ZSCORE"].astype(float).values


# Calculate spread
def calculate_spread(series_1, series_2, hedge_ratio):
    spread = pd.Series(series_1) - (pd.Series(series_2) * hedge_ratio)
    return spread


# Calculate metrics
def calculate_metrics(series_1, series_2):
    coint_flag = 0
    coint_res = coint(series_1, series_2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]
    model = sm.OLS(series_1, series_2).fit()
    hedge_ratio = model.params[0]
    spread = calculate_spread(series_1, series_2, hedge_ratio)
    zscore_list = calculate_zscore(spread)
    if p_value < 0.5 and coint_t < critical_value:
        coint_flag = 1
    return (coint_flag, zscore_list.tolist())


# Get latest z-score
def get_latest_zscore():
    ## Get latest asset orderbook prices and add dummy price for latest
    #Get most recent price
    live_data()
 
    mid_price_1, _, _ = get_trade_details(pos_ticker, app.ask_price_dict, app.bid_price_dict)
    mid_price_2, _, _ = get_trade_details(neg_ticker, app.ask_price_dict, app.bid_price_dict)
    
    # Get latest price history
    series_1, series_2 = list(app.hist_dict[pos_ticker].Close), list(app.hist_dict[neg_ticker].Close)

    # Get z_score and confirm if hot
    if len(series_1) > 0 and len(series_2) > 0:

        # Replace last kline price with latest orderbook mid price
        series_1 = series_1[:-1]
        series_2 = series_2[:-1]
        series_1.append(mid_price_1)
        series_2.append(mid_price_2)

        # Get latest zscore
        coint_flag, zscore_list = calculate_metrics(series_1, series_2)
        zscore = zscore_list[-1]
        if zscore > 0 and coint_flag == 1:
            signal_sign_positive = True
        else:
            signal_sign_positive = False

        # Return output
        return (zscore, signal_sign_positive)

    # Return output if not true
    return
