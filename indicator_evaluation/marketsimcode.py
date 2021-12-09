"""  	   		   	 		  		  		    	 		 		   		 		     		   	 		  		  		    	 		 		   		 		  
Student Name: Liangtian Zhang (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: lzhang699 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903658227 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""


import numpy as np
import pandas as pd
from util import get_data


def compute_portvals(
    orders,
    symbol="JPM",
    port_val_name='Benchmark',
    start_val=100000,
    commission=0,
    impact=0,
):
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param orders_file: Path of the order file or the file object  		  	   		   	 		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  		  	   		   	 		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		   	 		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		   	 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		   	 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		   	 		  		  		    	 		 		   		 		  
    """
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    orders.sort_values(by="Date", inplace=True)
    start_date, end_date = parse_orders(orders)

    prices = get_data([symbol], pd.date_range(
        start_date, end_date))
    prices[port_val_name] = pd.Series(0.0, index=prices.index)

    # for this project, should only contain "JPM"
    holdings = {}
    total_cash = start_val

    for date, price_row in prices.iterrows():
        # execute transaction if any on a given date
        for date, order in orders.loc[date:date].iterrows():
            shares = order['order']
            adj_close = price_row[symbol]
            cost = commission + impact * adj_close * shares

            if shares == 0:
                continue

            if symbol in holdings:
                holdings[symbol] += shares
            else:
                holdings[symbol] = shares

            trans_total = -1 * shares * adj_close
            total_cash += trans_total - cost

        # values of all holdings daily
        holdings_val = 0
        for each_symbol in holdings:
            adj_close = price_row[each_symbol]
            holdings_val += adj_close * holdings[each_symbol]

        price_row[port_val_name] = total_cash + holdings_val

    return prices[[port_val_name]]


def parse_orders(orders):
    start_date = orders.index[0]
    end_date = orders.index[-1]

    return start_date, end_date


def author():
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		   	 		  		  		    	 		 		   		 		  
    """
    return "lzhang699"  # replace tb34 with your Georgia Tech username.
