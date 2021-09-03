# """
# (c) 2015 by Devpriya Dave and Tucker Balch.
# """

# """=================================================================================="""

# """Compute Global Statistics"""




import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.base import DataError
# def symbol_to_path(symbol, base_dir="data"):
#     """Return CSV file path given ticker symbol."""
#     return os.path.join(base_dir, "{}.csv".format(str(symbol)))


# def get_data(symbols, dates):
#     """Read stock data (adjusted close) for given symbols from CSV files."""
#     df = pd.DataFrame(index=dates)
#     if 'SPY' not in symbols:  # add SPY for reference, if absent
#         symbols.insert(0, 'SPY')

#     for symbol in symbols:
#         df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
#                               parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
#         df_temp = df_temp.rename(columns={'Adj Close': symbol})
#         df = df.join(df_temp)
#         if symbol == 'SPY':  # drop dates SPY did not trade
#             df = df.dropna(subset=["SPY"])
#     return df


# def plot_data(df, title="Stock prices"):
#     """Plot stock prices with a custom title and meaningful axis labels."""
#     ax = df.plot(title=title, fontsize=12)
#     ax.set_xlabel("Date")
#     ax.set_ylabel("Price")
#     plt.show()


# def test_run():
# 	# Read data
# 	dates = pd.date_range('2010-01-01', '2012-12-31')
# 	symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
# 	df = get_data(symbols, dates)
# 	plot_data(df)

# 	# Compute global statistics for each stock
# 	print(df.mean())
# 	print(df.median())
# 	print(df.std())


# if __name__ == "__main__":
#     test_run()

# """============================================================================="""

# """Computing Rolling Statistics"""


# def symbol_to_path(symbol, base_dir="data"):
#     """Return CSV file path given ticker symbol."""
#     return os.path.join(base_dir, "{}.csv".format(str(symbol)))


# def get_data(symbols, dates):
#     """Read stock data (adjusted close) for given symbols from CSV files."""
#     df = pd.DataFrame(index=dates)
#     if 'SPY' not in symbols:  # add SPY for reference, if absent
#         symbols.insert(0, 'SPY')

#     for symbol in symbols:
#         df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
#                               parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
#         df_temp = df_temp.rename(columns={'Adj Close': symbol})
#         df = df.join(df_temp)
#         if symbol == 'SPY':  # drop dates SPY did not trade
#             df = df.dropna(subset=["SPY"])
#     return df


# def test_run():
# 	# Read data
# 	dates = pd.date_range('2010-01-01', '2012-12-31')
# 	symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
# 	df = get_data(symbols, dates)

# 	# Plot SPY, retain matplotlib axis object
# 	ax = df['SPY'].plot(title="SPY rolling mean", label='SPY')

# 	# Compute rolling mean using a 20-day window
# 	rm_SPY = df['SPY'].rolling(window=20).mean()

# 	# Add rolling mean to same plot
# 	rm_SPY.plot(label='Rolling mean', ax=ax)

# 	# Add axis labels and legend
# 	ax.set_xlabel("Date")
# 	ax.set_ylabel("Price")
# 	ax.legend(loc='upper left')
# 	plt.show()


# if __name__ == "__main__":
#     test_run()

"""============================================================================="""

"""Bollinger Bands."""


# def symbol_to_path(symbol, base_dir="../data"):
#     """Return CSV file path given ticker symbol."""
#     return os.path.join(base_dir, "{}.csv".format(str(symbol)))


# def get_data(symbols, dates):
#     """Read stock data (adjusted close) for given symbols from CSV files."""
#     df = pd.DataFrame(index=dates)
#     if 'SPY' not in symbols:  # add SPY for reference, if absent
#         symbols.insert(0, 'SPY')

#     for symbol in symbols:
#         df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
#                               parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
#         df_temp = df_temp.rename(columns={'Adj Close': symbol})
#         df = df.join(df_temp)
#         if symbol == 'SPY':  # drop dates SPY did not trade
#             df = df.dropna(subset=["SPY"])

#     return df


# # def plot_data(df, title="Stock prices"):
# #     """Plot stock prices with a custom title and meaningful axis labels."""
# #     ax = df.plot(title=title, fontsize=12)
# #     ax.set_xlabel("Date")
# #     ax.set_ylabel("Price")
# #     plt.show()


# def get_rolling_mean(values, windows):
#     """Return rolling mean of given values, using specified window size."""
#     return values.rolling(windows).mean()


# def get_rolling_std(values, windows):
#     """Return rolling standard deviation of given values, using specified window size."""
#     # Quiz: Compute and return rolling standard deviation
#     return values.rolling(windows).std()


# def get_bollinger_bands(rm, rstd):
#     """Return upper and lower Bollinger Bands."""
#     # Quiz: Compute upper_band and lower_band
#     upper_band = rm + rstd * 2
#     lower_band = rm - rstd * 2
#     return upper_band, lower_band

# def test_run():
#     dates = pd.date_range('2012-01-01', '2012-12-31')
#     symbols = []
#     dfSPY = get_data(symbols, dates)

#     ax = dfSPY.plot(title="SPY Bollinger Bands", fontsize=12)
    
#     rolling_mean = get_rolling_mean(dfSPY['SPY'], windows=20)
#     rolling_std = get_rolling_std(dfSPY['SPY'], windows=20)
#     upper_band, lower_band = get_bollinger_bands(rolling_mean, rolling_std)

#     rolling_mean.plot(label='Rolling Mean', ax=ax)
#     upper_band.plot(label='upper band', ax=ax)
#     lower_band.plot(label='lower band', ax=ax)
#     plt.show()

    

# if __name__ == "__main__":
#     test_run()

# """============================================================================="""

# """Compute daily returns."""


def symbol_to_path(symbol, base_dir="../data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                              parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()


def compute_daily_returns(df):
    """Compute and return the daily return values."""
    # Quiz: Your code here
    # Note: Returned DataFrame must have the same number of rows
    daily_returns = df.copy()
    # daily_returns[1:] = (df[1:] / df[:-1].values) - 1 # compute daily returns for row 1 onwards
    daily_returns = (df / df.iloc[0]) - 1  # much easier with Pandas!
    daily_returns.iloc[0, :] = 0  # Pandas leaves the 0th row full of Nans
    return daily_returns


def test_run():
    # Read data
    dates = pd.date_range('2012-07-01', '2012-07-31')  # one month only
    symbols = ['SPY', 'XOM']
    df = get_data(symbols, dates)
    plot_data(df)

    # Compute daily returns
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")


if __name__ == "__main__":
    test_run()
