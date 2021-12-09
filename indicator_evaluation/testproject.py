"""
Student Name: Liangtian Zhang (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: lzhang699 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903658227 (replace with your GT ID) 
"""
import datetime as dt
from os import name
import pandas as pd
import TheoreticallyOptimalStrategy as tos
from indicators import MACD, bollinger_bands, golden_cross, momentum, percent_B, rolling_mean, ema
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
from util import get_data


def author():
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		   	 		  		  		    	 		 		   		 		  
    """
    return "lzhang699"  # replace tb34 with your Georgia Tech username.


def compute_stats(port_val):
    daily_returns = port_val.copy()
    # compute daily returns for row 1 onwards
    daily_returns[1:] = (port_val[1:] / port_val[:-1].values) - 1
    daily_returns.iloc[0] = 0  # Pandas leaves the 0th row full of Nans

    cumm_return = (port_val.iloc[-1] / port_val.iloc[0]) - 1
    daily_returns_std = daily_returns.std()
    daily_returns_avg = daily_returns.mean()
    return cumm_return, daily_returns_std, daily_returns_avg


if __name__ == "__main__":
    symbol = 'JPM'
    # 2008/1/1 is not a trading day
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    dates = pd.date_range(sd, ed)
    window = 14

    # Benchmark

    starting_shares = 1000
    orders = pd.DataFrame(index=dates, columns=['order'])
    orders.index.name = 'Date'
    orders['order'] = 0
    orders.loc[orders.index[1], 'order'] = 1000

    benchmark_port = compute_portvals(
        orders, symbol, port_val_name='Benchmark')
    normed_benchmark_port = benchmark_port / benchmark_port.iloc[0]

    # TheoreticallyOptimalStrategy
    optimal_orders = tos.testPolicy(symbol=symbol, sd=dt.datetime(2008, 1, 1),
                                    ed=dt.datetime(2009, 12, 31))
    optimal_port = compute_portvals(
        optimal_orders, symbol, port_val_name='Optimal')
    normed_optimal_port = optimal_port / optimal_port.iloc[0]

    ax = normed_benchmark_port.plot(
        color='green', title='Benchmark vs Optimal Portfolio')
    normed_optimal_port.plot(ax=ax, color='red')
    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Values')
    plt.savefig('theoretically_optimal_strategy.png')
    plt.close()

    # print("Date Range: {} to {}".format(sd, ed))
    cumm_return, daily_returns_std, daily_returns_avg, = compute_stats(
        benchmark_port)

    print("Cumulative Return of Benchmark: {}".format(cumm_return))
    print("Standard Deviation of Benchmark: {}".format(daily_returns_std))
    print("Average Daily Return of Benchmark: {}".format(daily_returns_avg))

    cumm_return, daily_returns_std, daily_returns_avg, = compute_stats(
        optimal_port)

    print("Cumulative Return of Optimal Strategy: {}".format(cumm_return))
    print("Standard Deviation of Optimal Strategy: {}".format(daily_returns_std))
    print("Average Daily Return of Optimal Strategy: {}".format(daily_returns_avg))

    # Indicators
    # SMA
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[[symbol]]
    normed_prices = prices / prices.iloc[0]
    normed_prices.rename(
        columns={symbol: 'Normalized {}'.format(symbol)}, inplace=True)
    sma = rolling_mean(symbol, sd, ed, window)
    normed_sma = sma / sma.iloc[0]
    normed_sma.rename(columns={'SMA': 'Normalized SMA'}, inplace=True)
    price_over_sma = pd.DataFrame()
    price_over_sma['Price / SMA'] = prices[symbol] / sma['SMA']

    ax = normed_prices.plot(title='Simple Move Average', color='lightblue')
    normed_sma.plot(ax=ax, color='lightgreen')
    price_over_sma.plot(ax=ax, color='darkorange')
    plt.axhline(y=0.95, color='r', linestyle='dotted')
    plt.axhline(y=1.05, color='g', linestyle='dotted')
    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('Normalized {} Prices'.format(symbol))
    plt.savefig('price_over_sma.png')
    plt.close()

    # Bollinger Band
    ax = prices.plot(title='Bollinger Band', color='lightblue')
    sma.plot(label='SMA', ax=ax)

    upper, lower = bollinger_bands(symbol, sd, ed, window)
    upper.plot(ax=ax, color='green')
    lower.plot(ax=ax, color='red')
    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('{} Prices'.format(symbol))
    plt.savefig('bollinger_band.png')
    plt.close()

    percent_B = percent_B(symbol, sd, ed, window)
    percent_B.plot(title='% B', color='orange')
    plt.axhline(y=100, color='blue', linestyle='dotted')
    plt.axhline(y=50, color='blue', linestyle='dotted')
    plt.axhline(y=00, color='blue', linestyle='dotted')
    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('Percentage')
    plt.savefig('percent_b.png')
    plt.close()

    # Momentum
    ax = normed_prices.plot(title='Momentum', color='lightblue')
    momentum = momentum(symbol, sd, ed, window)
    momentum.plot(ax=ax, color='orange')
    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('Normalized {} Prices & Momentum'.format(symbol))
    plt.savefig('momentum.png')
    plt.close()

    # EMA
    ax = prices.plot(title='Exponential Moving Average', color='lightblue')
    ema = ema(symbol, sd, ed, window)
    ema.plot(ax=ax, color='orange')
    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('{} Prices & EMA'.format(symbol))
    plt.savefig('ema.png')
    plt.close()

    # MACD
    ax = normed_prices.plot(
        title='Moving Average Convergence Divergence', color='lightblue')
    macd, macd_signal = MACD(symbol, sd, ed)
    macd.plot(ax=ax, color='orange')
    macd_signal.plot(ax=ax)
    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('Normalized {} Prices & MACD'.format(symbol))
    plt.savefig('macd.png')
    plt.close()

    # Golden Cross
    ax = prices.plot(title='Golden/Death Cross', color='lightblue')
    ema_50, ema_200 = golden_cross(symbol, sd, ed)
    ema_50.plot(ax=ax, color='orange')
    ema_200.plot(ax=ax)
    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('{} Prices'.format(symbol))
    plt.savefig('golden_cross.png')
    plt.close()
