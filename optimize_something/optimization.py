""""""
"""MC1-P2: Optimize a portfolio.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		   	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		   	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		   	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		   	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 		  		  		    	 		 		   		 		  
or edited.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		   	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		   	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Liangtian Zhang (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: lzhang699 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903658227 (replace with your GT ID) 		  	   		   	 		  		  		    	 		 		   		 		  
"""


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality




import pandas as pd
import scipy.optimize as spo
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from util import get_data, plot_data
def optimize_portfolio(
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 1, 1),
    syms=["GOOG", "AAPL", "GLD", "XOM"],
    gen_plot=False,
):
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe  		  	   		   	 		  		  		    	 		 		   		 		  
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of  		  	   		   	 		  		  		    	 		 		   		 		  
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take  		  	   		   	 		  		  		    	 		 		   		 		  
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and  		  	   		   	 		  		  		    	 		 		   		 		  
    statistics.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 		  		  		    	 		 		   		 		  
    :type sd: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 		  		  		    	 		 		   		 		  
    :type ed: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
    :param syms: A list of symbols that make up the portfolio (note that your code should support any  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol in the data directory)  		  	   		   	 		  		  		    	 		 		   		 		  
    :type syms: list  		  	   		   	 		  		  		    	 		 		   		 		  
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your  		  	   		   	 		  		  		    	 		 		   		 		  
        code with gen_plot = False.  		  	   		   	 		  		  		    	 		 		   		 		  
    :type gen_plot: bool  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,  		  	   		   	 		  		  		    	 		 		   		 		  
        standard deviation of daily returns, and Sharpe ratio  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: tuple  		  	   		   	 		  		  		    	 		 		   		 		  
    """

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    # data cleansing
    prices_all.fillna(method='ffill', inplace=True)
    prices_all.fillna(method='bfill', inplace=True)
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

    # assuming long positions only
    days = 252
    # assuming risk-free return is zero
    risk_free_return = 0

    allocs_length = len(syms)
    allocs_guess = np.asarray([1 / allocs_length] * allocs_length)
    bounds = [(0, 1) for i in range(allocs_length)]
    constraints = ({
        'type': 'eq',
        'fun': lambda x:  np.sum(x) - 1,
    })
    min_result = spo.minimize(
        sr_min, allocs_guess, args=(prices, days), bounds=bounds, constraints=constraints, method='SLSQP', options={'disp': True})
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    allocs = min_result.x
    daily_returns = find_daily_returns(allocs, prices)
    port_val_normed = find_port_val_normed(allocs, prices)
    cr = port_val_normed[-1] / port_val_normed[0] - 1
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    sr = np.sqrt(days) * adr / sddr

    prices_SPY_normed = prices_SPY / prices_SPY.iloc[0]

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat(
            [port_val_normed, prices_SPY_normed], keys=["Portfolio", "SPY"], axis=1
        )
        ax = df_temp.plot(title='Optimized Portfolio vs SPY', fontsize=12, grid=True)
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Price")
        # plt.ylim([-256, 100])
        # plt.legend()
        plt.show()
        plt.savefig('portfolio_vs_spy.png')
        plt.close()

    return allocs, cr, adr, sddr, sr


# minimizer function
def sr_min(allocs, prices, days):
    daily_returns = find_daily_returns(allocs, prices)

    adr = daily_returns.mean()
    sddr = daily_returns.std()

    return -np.sqrt(days) * adr / sddr


def find_daily_returns(allocs, prices):
    port_val_normed = find_port_val_normed(allocs, prices)
    daily_returns = port_val_normed.copy()
    daily_returns[1:] = (port_val_normed[1:] / port_val_normed[:-1].values) - 1 # compute daily returns for row 1 onwards
    daily_returns.iloc[0] = 0  # Pandas leaves the 0th row full of Nans
    print(daily_returns)
    return daily_returns


def find_port_val_normed(allocs, prices):
    # normalized price
    price_normed = prices / prices.iloc[0]

    # 1st row represents initial allocation
    price_alloced = price_normed * allocs
    port_val_normed = price_alloced.sum(axis=1)

    return port_val_normed


def test_code():
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    This function WILL NOT be called by the auto grader.  		  	   		   	 		  		  		    	 		 		   		 		  
    """

    # start_date = dt.datetime(2009, 1, 1)
    # end_date = dt.datetime(2010, 1, 1)
    # symbols = ["GOOG", "AAPL", "GLD", "XOM", "IBM"]

    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ["IBM", "X", "GLD", "JPM"]
    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True
    )

    # Print statistics
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Symbols: {symbols}")
    print(f"Allocations:{allocations}")
    print(f"Sharpe Ratio: {sr}")
    print(f"Volatility (stdev of daily returns): {sddr}")
    print(f"Average Daily Return: {adr}")
    print(f"Cumulative Return: {cr}")


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
