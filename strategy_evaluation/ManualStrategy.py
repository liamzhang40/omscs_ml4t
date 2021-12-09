"""  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Liangtian Zhang (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: lzhang699 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903658227 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""

import datetime as dt
from indicators import MACD, golden_cross, momentum, percent_B, rolling_mean
from util import get_data
import pandas as pd
import numpy as np


def testPolicy(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
    window = 14

    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]

    sma = rolling_mean(symbol, sd, ed, window)
    b_p = percent_B(symbol, sd, ed, window)
    mo = momentum(symbol, sd, ed, window)

    sma['Signal'] = 0
    sma['Signal'] = np.select(
        condlist=[prices / sma['SMA'] > 1.05, prices / sma['SMA'] < 0.95],
        choicelist=[-1, 1], default=0)

    b_p['Signal'] = 0
    b_p['Signal'] = np.select(
        condlist=[(mo['Momentum'] < 0) & (b_p['%B'] > 0),
                  (mo['Momentum'] > 0) & (b_p['%B'] < 0)],
        choicelist=[-1, 1], default=0)

    sma_50, sma_200 = golden_cross(symbol, sd, ed)
    # g_c = sma_50 - sma_200
    sma_50['Signal'] = np.select(
        condlist=[(sma_50[['SMA']] > sma_200[['SMA']])
                  & (sma_50[['SMA']].shift() < sma_200[['SMA']].shift()),
                  (sma_50[['SMA']] < sma_200[['SMA']])
                  & (sma_50[['SMA']].shift() > sma_200[['SMA']].shift())],
        choicelist=[1, -1], default=0)
    g_c = sma_50[['Signal']]

    macd_raw, macd_signal = MACD(symbol, sd, ed)
    # macd = macd_raw - macd_signal
    macd_raw['Signal'] = np.select(
        condlist=[(macd_raw[['MACD']] > macd_signal[['MACD']])
                  & (macd_raw[['MACD']].shift() < macd_signal[['MACD']].shift()),
                  (macd_raw[['MACD']] < macd_signal[['MACD']])
                  & (macd_raw[['MACD']].shift() > macd_signal[['MACD']].shift())],
        choicelist=[1, -1], default=0)
    macd = macd_raw[['Signal']]

    orders = []
    position = 0

    for i in range(len(prices.index) - 1):
        sma_signal = sma['Signal'].iloc[i]
        b_p_signal = b_p['Signal'].iloc[i]

        # g_c_signal_remove = -1 if (g_c.iloc[i] >= 0).bool() and (g_c.iloc[i + 1] < 0).bool() or (g_c.iloc[i] > 0).bool() and (g_c.iloc[i + 1] <= 0).bool(
        # ) else (1 if (g_c.iloc[i] < 0).bool() and (g_c.iloc[i + 1] >= 0).bool() or (g_c.iloc[i] <= 0).bool() and (g_c.iloc[i + 1] > 0).bool() else 0)
        g_c_signal = g_c['Signal'].iloc[i + 1]

        # macd_signal_remove = -1 if (macd.iloc[i] > 0).bool() and (macd.iloc[i + 1] <= 0).bool() or (macd.iloc[i] >= 0).bool() and (macd.iloc[i + 1] < 0).bool(
        # ) else (1 if (macd.iloc[i] < 0).bool() and (macd.iloc[i + 1] >= 0).bool() or (macd.iloc[i] <= 0).bool() and (macd.iloc[i + 1] > 0).bool() else 0)
        macd_signal = macd['Signal'].iloc[i + 1]

        order_type = sma_signal * 0.2 + b_p_signal * \
            0.2 + g_c_signal * 0.3 + macd_signal * 0.3

        if order_type > 0:
            order = buy(position)
        elif order_type < 0:
            order = sell(position)
        else:
            order = 0

        orders.append(order)
        position += order

    orders.append(-position)
    orders_df = pd.DataFrame(
        data=orders, index=prices.index, columns=['order'])
    orders_df.index.name = 'Date'

    return orders_df


def buy(position):
    if position == 0:
        return 1000
    elif position > 0:
        return 0
    elif position < 0:
        return 2000


def sell(position):
    if position == 0:
        return -1000
    elif position > 0:
        return -2000
    elif position < 0:
        return 0


def author():
    return 'lzhang699'  # replace tb34 with your Georgia Tech username.
