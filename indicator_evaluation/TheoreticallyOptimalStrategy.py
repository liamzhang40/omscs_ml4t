"""
Student Name: Liangtian Zhang (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: lzhang699 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903658227 (replace with your GT ID) 

Use the time period January 1, 2008, to December 31, 2009.  
Starting cash is $100,000.  
Allowable positions are 1000 shares long, 1000 shares short, 0 shares. (You may trade up to 2000 shares at a time as long as you maintain these holding requirements.)  
Benchmark: The performance of a portfolio starting with $100,000 cash, investing in 1000 shares of JPM, and holding that position.  
Transaction costs for TheoreticallyOptimalStrategy:  
Commission: $0.00
Impact: 0.00. 
"""
import datetime as dt
import pandas as pd


from util import get_data


def author():
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		   	 		  		  		    	 		 		   		 		  
    """
    return "lzhang699"  # replace tb34 with your Georgia Tech username.


def testPolicy(
    symbol="JPM",
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 12, 31),
    sv=100000
):
    dates = pd.date_range(sd, ed)
    orders = []
    position = 0

    prices = get_data([symbol], dates)
    prices = prices[symbol]

    for i in range(len(prices.index) - 1):
        price_current_date = prices[i]
        price_next_date = prices[i + 1]
        if price_next_date > price_current_date:
            order = buy(position)
        else:
            order = sell(position)

        orders.append(order)
        position += order

    # last day sell if position is positive
    # buy back if position is negative
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
