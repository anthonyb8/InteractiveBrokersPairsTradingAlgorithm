from func_cointegration import calculate_cointegration
from func_cointegration import calculate_spread
from func_cointegration import calculate_zscore
import matplotlib.pyplot as plt
import pandas as pd


# Plot prices and trends
def plot_trends(sym_1, sym_2, price_data):
    
    prices_1 = list(price_data[sym_1].Close)
    prices_2 = list(price_data[sym_2].Close)
    
    #Check that Series are sames length
    if len(prices_1) > len(prices_2):
        prices_1 = prices_1[:-(len(prices_1) - len(prices_2))]
    elif len(prices_1) < len(prices_2):
        prices_2 = prices_2[:-(len(prices_2) - len(prices_1))]

    # Get spread and zscore
    coint_flag, p_value, t_value, c_value, hedge_ratio, zero_crossing = calculate_cointegration(prices_1, prices_2)
    spread = calculate_spread(prices_1, prices_2, hedge_ratio)
    zscore = calculate_zscore(spread)

    # Calculate percentage changes
    df = pd.DataFrame(columns=[sym_1, sym_2])
    df[sym_1] = prices_1
    df[sym_2] = prices_2
    df[f"{sym_1}_pct"] = df[sym_1] / prices_1[0]
    df[f"{sym_2}_pct"] = df[sym_2] / prices_2[0]
    series_1 = df[f"{sym_1}_pct"].astype(float).values
    series_2 = df[f"{sym_2}_pct"].astype(float).values

    # Plot charts
    fig, axs = plt.subplots(3, figsize=(16, 8))
    fig.suptitle(f"Price / Spread / Z-Score - {sym_1} vs {sym_2}")
    axs[0].plot(series_1)
    axs[0].plot(series_2)
    axs[1].plot(spread)
    axs[2].plot(zscore)
    plt.show()