"""
Student Name: Liangtian Zhang (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: lzhang699 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903658227 (replace with your GT ID) 

5 technical indicators
"""
import datetime as dt
import pandas as pd
from util import get_data


def get_days_ahead(symbol, sd, ed, window):
    # to ensure that enough dates are available for date 1
    delta = dt.timedelta(window * 2)
    extedned_sd = sd - delta
    prices = get_data([symbol], pd.date_range(extedned_sd, ed))
    return prices[[symbol]]


def rolling_mean(symbol, sd, ed, window):
    prices = get_days_ahead(symbol, sd, ed, window)

    output = prices.rolling(window).mean()
    output.rename(columns={symbol: 'SMA'}, inplace=True)
    return output.truncate(before=sd)


def rolling_std(symbol, sd, ed, window):
    prices = get_days_ahead(symbol, sd, ed, window)

    output = prices.rolling(window).std()
    output.rename(columns={symbol: 'Rolling Standard Deviation'}, inplace=True)
    return output.truncate(before=sd)


def percent_B(symbol, sd, ed, window):
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[[symbol]]
    upper_band, lower_band = bollinger_bands(symbol, sd, ed, window)

    prices.rename(columns={symbol: '%B'}, inplace=True)
    upper_band.rename(columns={'Upper': '%B'}, inplace=True)
    lower_band.rename(columns={'Lower': '%B'}, inplace=True)
    output = (prices - lower_band) / (upper_band - lower_band) * 100
    return output


def bollinger_bands(symbol, sd, ed, window):
    rm = rolling_mean(symbol, sd, ed, window)
    rstd = rolling_std(symbol, sd, ed, window)

    upper_band = rm.rename(columns={'SMA': 'Upper'}) + \
        rstd.rename(columns={'Rolling Standard Deviation': 'Upper'}) * 2
    lower_band = rm.rename(columns={'SMA': 'Lower'}) - \
        rstd.rename(columns={'Rolling Standard Deviation': 'Lower'}) * 2
    return upper_band, lower_band


def momentum(symbol, sd, ed, window):
    prices = get_days_ahead(symbol, sd, ed, window)

    output = (prices / prices.shift(window)) - 1
    output.rename(columns={symbol: 'Momentum'}, inplace=True)
    return output.truncate(before=sd)


def ema(symbol, sd, ed, window):
    prices = get_days_ahead(symbol, sd, ed, window)
    
    output = prices.ewm(span=window, adjust=False).mean()
    output.rename(columns={symbol: 'EMA'}, inplace=True)
    return output.truncate(before=sd)


def MACD(symbol, sd, ed):
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[[symbol]]

    ema_12 = prices.ewm(span=12, adjust=False).mean()
    ema_26 = prices.ewm(span=26, adjust=False).mean()
    macd_raw = ema_12 - ema_26
    macd_signal = macd_raw.ewm(span=9, adjust=False).mean()
    macd_raw.rename(columns={symbol: 'MACD'}, inplace=True)
    macd_signal.rename(columns={symbol: 'MACD'}, inplace=True)
    
    return macd_raw.truncate(before=sd), macd_signal.truncate(before=sd)


def golden_cross(symbol, sd, ed):
    sma_50 = rolling_mean(symbol, sd, ed, 50)
    sma_200 = rolling_mean(symbol, sd, ed, 200)

    # sma_50.rename(columns={'SMA': 'SMA 50'}, inplace=True)
    # sma_200.rename(columns={'SMA': 'SMA 200'}, inplace=True)
    return sma_50, sma_200

def author():
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		   	 		  		  		    	 		 		   		 		  
    """
    return "lzhang699"  # replace tb34 with your Georgia Tech username.
