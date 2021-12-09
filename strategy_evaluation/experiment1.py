from ManualStrategy import testPolicy
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd


def exp1(normed_benchmark_port_in_sample, normed_manual_port_in_sample, normed_benchmark_port_out_of_sample, normed_manual_port_out_of_sample):
    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    commission = 9.95
    impact = 0.005

    # Strategy Learner
    learner = StrategyLearner(
        verbose=False, impact=impact, commission=commission)  # constructor

    learner.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=100000)  # training phase

    # in sample
    in_sample_learner_trades = learner.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)  # testing phase
    in_sample_learner_port = compute_portvals(
        in_sample_learner_trades, symbol, port_val_name='In Sample Strategy Learner', commission=commission, impact=impact)
    in_sample_normed_learner_port = in_sample_learner_port / \
        in_sample_learner_port.iloc[0]

    ax = normed_benchmark_port_in_sample.plot(
        color='green', title='Benchmark vs Manual Strategy vs Strategy Learner In Sample')
    normed_manual_port_in_sample.plot(ax=ax, color='red')
    in_sample_normed_learner_port.plot(ax=ax, color='blue')
    plt.grid()
    plt.legend(loc='upper left')
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Values')
    plt.savefig('experiment_1_in_sample')
    # plt.show()
    plt.close()

    # out of sample
    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2011, 12, 31)

    out_of_sample_learner_trades = learner.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)  # testing phase
    out_of_sample_learner_port = compute_portvals(
        out_of_sample_learner_trades, symbol, port_val_name='Out of Sample Strategy Learner', commission=commission, impact=impact)
    out_of_sample_normed_learner_port = out_of_sample_learner_port / \
        out_of_sample_learner_port.iloc[0]

    ax = normed_benchmark_port_out_of_sample.plot(
        color='green', title='Benchmark vs Manual Strategy vs Strategy Learner Out of Sample')
    normed_manual_port_out_of_sample.plot(ax=ax, color='red')
    out_of_sample_normed_learner_port.plot(ax=ax, color='blue')
    plt.grid()
    plt.legend(loc='upper left')
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Values')
    plt.savefig('experiment_1_out_of_sample')
    # plt.show()
    plt.close()


def author():
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		   	 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		   	 		  		  		    	 		 		   		 		  
    """
    return "lzhang699"  # replace tb34 with your Georgia Tech username.
