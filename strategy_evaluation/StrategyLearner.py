""""""
"""  		  	   		   	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
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




import pandas as pd
import numpy as np
import util as ut
from indicators import MACD, golden_cross, momentum, percent_B, rolling_mean
import datetime as dt
from QLearner import QLearner
class StrategyLearner(object):
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		   	 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		   	 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		   	 		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		   	 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		   	 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		   	 		  		  		    	 		 		   		 		  
    """
    # constructor

    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		   	 		  		  		    	 		 		   		 		  
        """
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.qlearner = QLearner(
            # 3 ^ 4:  4 indicators
            num_states=81,
            num_actions=3,
            alpha=0.2,
            gamma=0.9,
            rar=0.98,
            radr=0.9,
            dyna=50,
            verbose=False,
        )

    # this method should create a QLearner, and train it for trading
    def add_evidence(
        self,
        symbol="JPM",
        sd=dt.datetime(2008, 1, 1),
        ed=dt.datetime(2009, 12, 31),
        sv=10000,
        timeout=20
    ):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Trains your strategy learner over a given time frame.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol to train on  		  	   		   	 		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		   	 		  		  		    	 		 		   		 		  
        """

        # add your code to do learning here
        window = 14

        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices = prices[symbol]

        sma = rolling_mean(symbol, sd, ed, window)
        b_p = percent_B(symbol, sd, ed, window)
        mo = momentum(symbol, sd, ed, window)

        sma['Signal'] = 0
        sma['Signal'] = np.select(
            condlist=[prices / sma['SMA'] > 1.05, prices / sma['SMA'] < 0.95],
            choicelist=[1, 2], default=0)

        b_p['Signal'] = 0
        b_p['Signal'] = np.select(
            condlist=[(mo['Momentum'] < 0) & (b_p['%B'] > 0),
                      (mo['Momentum'] > 0) & (b_p['%B'] < 0)],
            choicelist=[1, 2], default=0)

        sma_50, sma_200 = golden_cross(symbol, sd, ed)
        sma_50['Signal'] = np.select(
            condlist=[(sma_50[['SMA']] > sma_200[['SMA']])
                      & (sma_50[['SMA']].shift() < sma_200[['SMA']].shift()),
                      (sma_50[['SMA']] < sma_200[['SMA']])
                      & (sma_50[['SMA']].shift() > sma_200[['SMA']].shift())],
            choicelist=[1, -1], default=0)
        g_c = sma_50[['Signal']]

        macd_raw, macd_signal = MACD(symbol, sd, ed)
        macd_raw['Signal'] = np.select(
            condlist=[(macd_raw[['MACD']] > macd_signal[['MACD']])
                      & (macd_raw[['MACD']].shift() < macd_signal[['MACD']].shift()),
                      (macd_raw[['MACD']] < macd_signal[['MACD']])
                      & (macd_raw[['MACD']].shift() > macd_signal[['MACD']].shift())],
            choicelist=[1, -1], default=0)
        macd = macd_raw[['Signal']]

        prev_port_val = 0
        port_val = sv
        count = 0
        while (prev_port_val != port_val) & (count < timeout):
            prev_port_val = port_val
            count += 1
            position = 0
            cash = sv

            sma_indicator, b_p_indicator, g_c_indicator, macd_indicator = self.find_indicators(
                0, sma, b_p, g_c, macd)

            state = self.discretize(
                sma_indicator, b_p_indicator, g_c_indicator, macd_indicator)
            action = self.qlearner.querysetstate(state)

            for i in range(1, len(prices.index)):
                # cash and position after taking action from previous day / last iteration
                r, position, cash, order = self.transact(
                    prices[i - 1], prices[i], position, action, cash)

                if i == len(prices.index) - 1:
                    break
                # today's / current iteraction's indicators (to derive state)
                sma_indicator, b_p_indicator, g_c_indicator, macd_indicator = self.find_indicators(
                    i, sma, b_p, g_c, macd)
                # today's / current iteraction's state
                state = self.discretize(
                    sma_indicator, b_p_indicator, g_c_indicator, macd_indicator)
                action = self.qlearner.query(state, r)

            port_val = cash + position * prices[-1]

            if self.verbose:
                print(port_val)

    def testPolicy(
        self,
        symbol="JPM",
        sd=dt.datetime(2010, 1, 1),
        ed=dt.datetime(2011, 12, 31),
        sv=10000,
    ):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol that you trained on on  		  	   		   	 		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		   	 		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		   	 		  		  		    	 		 		   		 		  
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		   	 		  		  		    	 		 		   		 		  
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		   	 		  		  		    	 		 		   		 		  
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		   	 		  		  		    	 		 		   		 		  
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		   	 		  		  		    	 		 		   		 		  
        :rtype: pandas.DataFrame  		  	   		   	 		  		  		    	 		 		   		 		  
        """

        window = 14

        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        prices = prices[symbol]

        sma = rolling_mean(symbol, sd, ed, window)
        b_p = percent_B(symbol, sd, ed, window)
        mo = momentum(symbol, sd, ed, window)

        sma['Signal'] = 0
        sma['Signal'] = np.select(
            condlist=[prices / sma['SMA'] > 1.05, prices / sma['SMA'] < 0.95],
            choicelist=[1, 2], default=0)

        b_p['Signal'] = 0
        b_p['Signal'] = np.select(
            condlist=[(mo['Momentum'] < 0) & (b_p['%B'] > 0),
                      (mo['Momentum'] > 0) & (b_p['%B'] < 0)],
            choicelist=[1, 2], default=0)

        sma_50, sma_200 = golden_cross(symbol, sd, ed)
        sma_50['Signal'] = np.select(
            condlist=[(sma_50[['SMA']] > sma_200[['SMA']])
                      & (sma_50[['SMA']].shift() < sma_200[['SMA']].shift()),
                      (sma_50[['SMA']] < sma_200[['SMA']])
                      & (sma_50[['SMA']].shift() > sma_200[['SMA']].shift())],
            choicelist=[1, -1], default=0)
        g_c = sma_50[['Signal']]

        macd_raw, macd_signal = MACD(symbol, sd, ed)
        macd_raw['Signal'] = np.select(
            condlist=[(macd_raw[['MACD']] > macd_signal[['MACD']])
                      & (macd_raw[['MACD']].shift() < macd_signal[['MACD']].shift()),
                      (macd_raw[['MACD']] < macd_signal[['MACD']])
                      & (macd_raw[['MACD']].shift() > macd_signal[['MACD']].shift())],
            choicelist=[1, -1], default=0)
        macd = macd_raw[['Signal']]

        # turn off exploration
        self.qlearner.rar = -1
        orders = []
        position = 0

        for i in range(len(prices.index) - 1):
            sma_indicator, b_p_indicator, g_c_indicator, macd_indicator = self.find_indicators(
                i, sma, b_p, g_c, macd)

            state = self.discretize(
                sma_indicator, b_p_indicator, g_c_indicator, macd_indicator)

            action = self.qlearner.querysetstate(state)
            order = self.decode_action_to_order(action, position)
            position += order
            orders.append(order)

        orders.append(-position)
        orders_df = pd.DataFrame(
            data=orders, index=prices.index, columns=['order'])
        orders_df.index.name = 'Date'

        return orders_df

    def discretize(self, sma, b_p, g_c, macd):
        return sma + b_p * 3 + g_c * 9 + macd * 27

    def find_indicators(self, i, sma, b_p, g_c, macd):
        sma_indicator = sma['Signal'].iloc[i]
        b_p_indicator = b_p['Signal'].iloc[i]
        g_c_indicator = g_c['Signal'].iloc[i + 1]
        macd_indicator = macd['Signal'].iloc[i + 1]

        return sma_indicator, b_p_indicator, g_c_indicator, macd_indicator

    def transact(self, price_yesterday, price_today, position, action, cash):
        order = self.decode_action_to_order(action, position)

        new_position = position + order
        reward = new_position * \
            (price_today - price_yesterday) - \
            self.impact * order * price_yesterday
        cash -= order * price_yesterday

        return reward, new_position, cash, order

    def decode_action_to_order(self, action, position):
        if action == 0:
            order = self.sell(position)
        elif action == 1:
            order = 0
        else:
            order = self.buy(position)

        return order

    def buy(self, position):
        if position == 0:
            return 1000
        elif position > 0:
            return 0
        elif position < 0:
            return 2000

    def sell(self, position):
        if position == 0:
            return -1000
        elif position > 0:
            return -2000
        elif position < 0:
            return 0

    def author(self):
        return 'lzhang699'  # replace tb34 with your Georgia Tech username.
