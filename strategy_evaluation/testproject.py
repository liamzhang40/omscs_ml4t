from matplotlib import pyplot as plt
from ManualStrategy import testPolicy
from StrategyLearner import StrategyLearner
from experiment1 import exp1
import pandas as pd
import datetime as dt
from experiment2 import exp2

from marketsimcode import compute_portvals


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


def find_long_short_entries(df_trades):
    long = []
    short = []
    position = 0
    for date in df_trades.index:
        trade = df_trades.loc[date]
        new_position = position + trade
        if position <= 0 and new_position > 0:
            long.append(date)
        elif position >= 0 and new_position < 0:
            short.append(date)

        position = new_position

    return long, short

def in_out_bench_manual_strategy():
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    dates = pd.date_range(sd, ed)
    symbol = 'JPM'
    commission = 9.95
    impact = 0.005

    # Benchmark In Sample
    starting_shares = 1000
    orders = pd.DataFrame(index=dates, columns=['order'])
    orders.index.name = 'Date'
    orders['order'] = 0
    orders.loc[orders.index[1], 'order'] = starting_shares
    benchmark_port_in_sample = compute_portvals(
        orders, symbol, port_val_name='Benchmark', commission=commission, impact=impact)
    normed_benchmark_port_in_sample = benchmark_port_in_sample / benchmark_port_in_sample.iloc[0]

    # Manual In Sample
    manual_orders = testPolicy(symbol=symbol, sd=sd,
                               ed=ed)
    manual_port_in_sample = compute_portvals(
        manual_orders, symbol, port_val_name='Manual Strategy', commission=commission, impact=impact)
    normed_manual_port_in_sample = manual_port_in_sample / manual_port_in_sample.iloc[0]
    long_in_sample, short_in_sample = find_long_short_entries(
        manual_orders['order'])

    # Manual Out of Sample
    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2011, 12, 31)
    dates = pd.date_range(sd, ed)

    starting_shares = 1000
    orders = pd.DataFrame(index=dates, columns=['order'])
    orders.index.name = 'Date'
    orders['order'] = 0
    orders.loc[orders.index[3], 'order'] = starting_shares
    benchmark_port_out_of_sample = compute_portvals(
        orders, symbol, port_val_name='Benchmark', commission=commission, impact=impact)
    normed_benchmark_port_out_of_sample = benchmark_port_out_of_sample / benchmark_port_out_of_sample.iloc[0]

    # Benchmark Out of Sample
    manual_orders = testPolicy(symbol=symbol, sd=sd,
                               ed=ed)
    manual_port_out_of_sample = compute_portvals(
        manual_orders, symbol, port_val_name='Manual Strategy', commission=commission, impact=impact)
    normed_manual_port_out_of_sample = manual_port_out_of_sample / manual_port_out_of_sample.iloc[0]
    long_out_of_sample, short_out_of_sample = find_long_short_entries(
        manual_orders['order'])

    return benchmark_port_in_sample, \
        normed_benchmark_port_in_sample, \
        manual_port_in_sample, \
        normed_manual_port_in_sample, \
        long_in_sample, \
        short_in_sample, \
        benchmark_port_out_of_sample, \
        normed_benchmark_port_out_of_sample, \
        manual_port_out_of_sample, \
        normed_manual_port_out_of_sample, \
        long_out_of_sample, \
        short_out_of_sample


def exp0(
        benchmark_port_in_sample,
        normed_benchmark_port_in_sample,
        manual_port_in_sample,
        normed_manual_port_in_sample,
        long_in_sample,
        short_in_sample,
        benchmark_port_out_of_sample,
        normed_benchmark_port_out_of_sample,
        manual_port_out_of_sample,
        normed_manual_port_out_of_sample,
        long_out_of_sample,
        short_out_of_sample):

    ax = normed_benchmark_port_in_sample.plot(
        color='green', title='Benchmark vs Manual Strategy In Sample')
    normed_manual_port_in_sample.plot(ax=ax, color='red')
    plt.axvline(short_in_sample[0], color="black", ymax=0.8, label='short')
    for date in short_in_sample:
        plt.axvline(date, color="black", ymax=0.8)

    plt.axvline(long_in_sample[0], color="blue", label='long')
    for date in long_in_sample:
        plt.axvline(date, color="blue")
    plt.grid()
    plt.legend(loc='lower right')
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Values')
    plt.savefig('manual_strategy_in_sample')
    plt.close()

    cumm_return, daily_returns_std, daily_returns_avg, = compute_stats(
        benchmark_port_in_sample)
    print("In Sample ----------")
    print("Cumulative Return of Benchmark: {}".format(cumm_return.to_string()))
    print("Standard Deviation of Benchmark: {}".format(
        daily_returns_std.to_string()))
    print("Average Daily Return of Benchmark: {}".format(
        daily_returns_avg.to_string()))

    cumm_return, daily_returns_std, daily_returns_avg, = compute_stats(
        manual_port_in_sample)
    print("In Sample ----------")
    print("Cumulative Return of Manual Strategy: {}".format(
        cumm_return.to_string()))
    print("Standard Deviation of Manual Strategy: {}".format(
        daily_returns_std.to_string()))
    print("Average Daily Return of Manual Strategy: {}".format(
        daily_returns_avg.to_string()))


    ax = normed_benchmark_port_out_of_sample.plot(
        color='green', title='Benchmark vs Manual Strategy Out of Sample')
    normed_manual_port_out_of_sample.plot(ax=ax, color='red')
    plt.axvline(short_out_of_sample[0], color="black", ymax=0.8, label='short')
    for date in short_out_of_sample:
        plt.axvline(date, color="black", ymax=0.8)

    plt.axvline(long_out_of_sample[0], color="blue", label='long')
    for date in long_out_of_sample:
        plt.axvline(date, color="blue")
    plt.grid()
    plt.legend(loc='lower right')
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Values')
    plt.savefig('manual_strategy_out_of_sample')
    plt.close()

    cumm_return, daily_returns_std, daily_returns_avg, = compute_stats(
        benchmark_port_out_of_sample)
    print("Out of Sample ----------")
    print("Cumulative Return of Benchmark: {}".format(cumm_return.to_string()))
    print("Standard Deviation of Benchmark: {}".format(
        daily_returns_std.to_string()))
    print("Average Daily Return of Benchmark: {}".format(
        daily_returns_avg.to_string()))

    cumm_return, daily_returns_std, daily_returns_avg, = compute_stats(
        manual_port_out_of_sample)
    print("Out of Sample ----------")
    print("Cumulative Return of Manual Strategy: {}".format(
        cumm_return.to_string()))
    print("Standard Deviation of Manual Strategy: {}".format(
        daily_returns_std.to_string()))
    print("Average Daily Return of Manual Strategy: {}".format(
        daily_returns_avg.to_string()))


if __name__ == "__main__":
    # Manual Strategy
    benchmark_port_in_sample, \
    normed_benchmark_port_in_sample, \
    manual_port_in_sample, \
    normed_manual_port_in_sample, \
    long_in_sample, \
    short_in_sample, \
    benchmark_port_out_of_sample, \
    normed_benchmark_port_out_of_sample, \
    manual_port_out_of_sample, \
    normed_manual_port_out_of_sample, \
    long_out_of_sample, \
    short_out_of_sample = in_out_bench_manual_strategy()

    exp0(
        benchmark_port_in_sample,
        normed_benchmark_port_in_sample,
        manual_port_in_sample,
        normed_manual_port_in_sample,
        long_in_sample,
        short_in_sample,
        benchmark_port_out_of_sample,
        normed_benchmark_port_out_of_sample,
        manual_port_out_of_sample,
        normed_manual_port_out_of_sample,
        long_out_of_sample,
        short_out_of_sample)

    # Strategy Learner

    # Experiment 1
    exp1(normed_benchmark_port_in_sample, normed_manual_port_in_sample,
         normed_benchmark_port_out_of_sample, normed_manual_port_out_of_sample)

    # Experiment 2
    exp2()
