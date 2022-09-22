#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 22:13:03 2022

@author: anthony
"""

from config_execution_api import pos_ticker, neg_ticker
from config_ws_connect import app
from func_save_status import save_status
from func_price_calls import historical_data
from func_position_calls import orders_positions
from func_trade_management import manage_new_trades

from func_close_positions import close_all_positions
from func_get_zscore import get_latest_zscore
import time


""" RUN STATBOT """
if __name__ == "__main__":
    # Initial printout
    print("StatBot initiated...")

    # Initialise variables
    status_dict = {"message": "starting..."}
    order_long = {}
    order_short = {}
    signal_sign_positive = ""
    signal_side = ""
    trade_progress = 0 ## 0 = no position open, 1= position open, 2 = close position

    # Save status
    save_status(status_dict)
    
    # Get historical Data
    historical_data()
    while not app.hist_data_event:
        continue

    # Commence bot
    print("Seeking trades...")
    while True:
             
        # Check if open trades already exist
        no_positions = not any(orders_positions())
    
        # Save status
        status_dict["message"] = "Initial checks made..."
        save_status(status_dict)
        
        # Check for signal and place new trades
        if no_positions:
            
            if trade_progress == 0:
                status_dict["message"] = "Managing new trades..."
                save_status(status_dict)
                trade_progress, signal_side = manage_new_trades(trade_progress) 
        
            # Managing open kill switch if positions change or should reach 2
            # Check for signal to be false
            if trade_progress == 1:
    
                # Get and save the latest z-score
                zscore, signal_sign_positive = get_latest_zscore()
    
                # Close positions
                if signal_side == "positive" and zscore < 0:
                    trade_progress = 2
                if signal_side == "negative" and zscore >= 0:
                    trade_progress = 2
    
                # Put back to zero if trades are closed
                if no_positions and trade_progress != 2:
                    trade_progress = 0
    
            # Close all active orders and positions
            if trade_progress == 2:
                print("Closing all positions...")
                status_dict["message"] = "Closing existing trades..."
                save_status(status_dict)
                trade_progress = close_all_positions()
    
        time.sleep(15)