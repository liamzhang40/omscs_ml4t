from ManualStrategy import testPolicy
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd


def compute_stats(port_val):
    daily_returns = port_val.copy()
    # compute daily returns for row 1 onwards
    daily_returns[1:] = (port_val[1:] / port_val[:-1].values) - 1
    daily_returns.iloc[0] = 0  # Pandas leaves the 0th row full of Nans

    cumm_return = (port_val.iloc[-1] / port_val.iloc[0]) - 1
    daily_returns_std = daily_returns.std()
    daily_returns_avg = daily_returns.mean()
    return cumm_return, daily_returns_std, daily_returns_avg


def find_trade_dates(df_trades):
    dates = []
    for date in df_trades.index:
        trade = df_trades.loc[date]
        if trade != 0:
            dates.append(date)

    return dates


def exp2():
    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    commission = 0
    impact = 0

    # Strategy Learner impact 0
    learner = StrategyLearner(
        verbose=False, impact=impact, commission=commission)  # constructor

    learner.add_evidence(symbol=symbol, sd=sd, ed=ed,
                         sv=100000)  # training phase

    learner_trades = learner.testPolicy(
        symbol=symbol, sd=sd, ed=ed, sv=100000)  # testing phase
    learner_port = compute_portvals(
        learner_trades, symbol, port_val_name='impact = {}'.format(impact), commission=commission, impact=impact)
    normed_learner_port_1 = learner_port / \
        learner_port.iloc[0]

    dates = find_trade_dates(learner_trades['order'])
    ax = normed_learner_port_1.plot(
        color='green', title='Learner Strategy Impact = {}'.format(impact))
    plt.axvline(dates[0], color="black", label='trades')
    for date in dates:
        plt.axvline(date, color="black")

    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Values')
    plt.savefig('experiment_2_impact_0')
    plt.close()

    cumm_return, daily_returns_std, _ = compute_stats(
        learner_port)
    print("Cumulative Return of impact = {}: {}".format(
        impact, cumm_return.to_string()))
    print("Standard Deviation of impact = {}: {}".format(
        impact, daily_returns_std.to_string()))

    # Strategy Learner impact 0.005
    impact = 0.05
    learner = StrategyLearner(
        verbose=False, impact=impact, commission=commission)  # constructor

    learner.add_evidence(symbol=symbol, sd=sd, ed=ed,
                         sv=100000, timeout=30)  # training phase

    learner_trades = learner.testPolicy(
        symbol=symbol, sd=sd, ed=ed, sv=100000)  # testing phase
    learner_port = compute_portvals(
        learner_trades, symbol, port_val_name='impact = {}'.format(impact), commission=commission, impact=impact)
    normed_learner_port_2 = learner_port / \
        learner_port.iloc[0]

    dates = find_trade_dates(learner_trades['order'])
    ax = normed_learner_port_2.plot(
        color='green', title='Learner Strategy Impact = {}'.format(impact))
    plt.axvline(dates[0], color="black", label='trades')
    for date in dates:
        plt.axvline(date, color="black")

    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Values')
    plt.savefig('experiment_2_impact_05')
    plt.close()

    cumm_return, daily_returns_std, _ = compute_stats(
        learner_port)
    print("Cumulative Return of impact = {}: {}".format(
        impact, cumm_return.to_string()))
    print("Standard Deviation of impact = {}: {}".format(
        impact, daily_returns_std.to_string()))

    # Strategy Learner impact 0.01
    impact = 0.1
    learner = StrategyLearner(
        verbose=False, impact=impact, commission=commission)  # constructor

    learner.add_evidence(symbol=symbol, sd=sd, ed=ed,
                         sv=100000)  # training phase

    learner_trades = learner.testPolicy(
        symbol=symbol, sd=sd, ed=ed, sv=100000)  # testing phase
    learner_port = compute_portvals(
        learner_trades, symbol, port_val_name='impact = {}'.format(impact), commission=commission, impact=impact)
    normed_learner_port_3 = learner_port / \
        learner_port.iloc[0]

    dates = find_trade_dates(learner_trades['order'])
    ax = normed_learner_port_3.plot(
        color='green', title='Learner Strategy Impact = {}'.format(impact))
    if len(dates) > 0:
        plt.axvline(dates[0], color="black", label='trades')
    for date in dates:
        plt.axvline(date, color="black")

    plt.grid()
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Values')
    plt.savefig('experiment_2_impact_01')
    plt.close()

    cumm_return, daily_returns_std, _ = compute_stats(
        learner_port)
    print("Cumulative Return of impact = {}: {}".format(
        impact, cumm_return.to_string()))
    print("Standard Deviation of impact = {}: {}".format(
        impact, daily_returns_std.to_string()))


def author():
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		   	 		  		  		    	 		 		   		 		  
    """
    return "lzhang699"  # replace tb34 with your Georgia Tech username.
