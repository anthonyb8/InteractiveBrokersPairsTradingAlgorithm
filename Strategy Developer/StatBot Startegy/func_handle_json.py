import json
from config_strategy import file_name, ticker_file_name
from config_ws_connect import app
import pandas as pd
from datetime import date



# Store price histry for all available pairs
def store_price_history():
    # convert dataframes into dictionaries
    nested_dict = {key: app.hist_dict[key].to_dict(orient='index') for key in app.hist_dict.keys()}

    # Output prices to JSON
    if len(nested_dict) > 0:
        with open('/Users/anthony/python/IB_trading/StatBot/DataFiles/' + file_name, "w") as fp:
            json.dump(nested_dict, fp, indent=4)
        print("Prices saved successfully.")

    # Return output
    return

def open_price_history():
    with open('/Users/anthony/python/IB_trading/StatBot/DataFiles/' + file_name) as json_file:
        price_data = json.load(json_file)
    if len(price_data) > 0:
        # convert dictionaries into dataframes
        data = {key: pd.DataFrame(price_data[key]).T for key in price_data}
        return data

# Store price histry for all available pairs
def store_tickers():
    # Output prices to JSON
    if len(app.shortable_tickers) > 0:
        with open(ticker_file_name, "w") as fp:
            json.dump(app.shortable_tickers, fp, indent=4)
        print("Tradeable tickers saved successfully.")

    # Return output
    return

def open_tickers():
    with open(ticker_file_name) as json_file:
        tickers = json.load(json_file)
    if len(tickers) > 0:
        return tickers 
       