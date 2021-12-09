# Documentation
This README should help you run this project in your local enviromnent

## testproject.py
  This is core executable, it
  1. calls three major experiment files exp0, exp1, exp2
  2. generates all graphs and terminal outputs 

  The stock traded in here is by default 'JPM', start date 2008/01/01,
  end date 2009/12/31 as in sample data, start date 2010/01/01, end date 2011/12/31
  as out of sample data
  Run this file by 
  ```
  python testproject.py  
  ```

## indicators.py
  5 different indicators are implemented in this file with their helper functions
  * `rolling_mean`
  * `percent_B`
  * `momentum`
  * `ema`
  * `MACD`

  The first 4 functions expect 4 arguments
  * `symbol` ticker of a stock
  * `sd` start data
  * `ed` end data
  * `window` window for rolling stats
  `MACD` does not require `window`

  All functions return one or two dataframes with date index column and a column
  with respective stats value. For example, `rolling_mean` returns
  |Date|SMA|
  |-|-|
  |2008/01/02|23.4|
  |...|...|

  Note:
  `window` is also used to fill window * 2 days ahead of start date so that rolling
  metrics can be capture for the start date.

  import functions from this file to run them 
  ```
  from indicators import MACD, bollinger_bands, momentum, percent_B, rolling_mean, ema
  symbol = 'JPM' 
  sd = dt.datetime(2008, 1, 1)
  ed = dt.datetime(2009, 12, 31)
  window = 14

  sma = rolling_mean(symbol, sd, ed, window)
  percent_B = percent_B(symbol, sd, ed, window)
  ```


## StrategyLearner.py  
  `StrategyLearner` is a learner class implemented with a QLearner.
  This class can be intiated with the following parameters
  * `verbose` ticker of a stock
  * `impact` start data
  * `commission` end data

  `add_evidence` is a function to call when feeding training data
  This function does not return anything

  `testPolicy` returns a dataframe of orders with given start date
  and end date

  import functions from this file to run them 
  ```
  learner = StrategyLearner(
      verbose=False, impact=impact, commission=commission)  # constructor

  learner.add_evidence(symbol=symbol, sd=sd, ed=ed,
                        sv=100000)  # training phase

  learner_trades_1 = learner.testPolicy(
      symbol=symbol, sd=sd, ed=ed, sv=100000)  # testing phase
  ```

## QLearner.py
  `QLearner` is class utilized inside StrategyLearner.py

  ```
  qlearner = QLearner(
            num_states=81,
            num_actions=3,
            alpha=0.2,
            gamma=0.9,
            rar=0.98,
            radr=0.9,
            dyna=50,
            verbose=False,
        )

  qlearner.querysetstate(state)
  qlearner.query(state, r)
  ```

## marketsimcode.py
  Utility function that takes in a dataframe of orders and return
  a dataframe of portfolio

  ```
  in_sample_learner_port = compute_portvals(
    in_sample_learner_trades, symbol, port_val_name='In Sample Strategy Learner', commission=commission, impact=impact)
  ```

## ManualStrategy.py
  `test_policy` returns a dataframe of orders based on stock prices
  using indicators

## experiment1.py
  A script that generates chart and terminal output to compare the performance of
  Benchmark, Manual Strategy and Strategy Learner

## experiment2.py
  A script that generates chart and terminal output to compare the performance of
  Strategy Learner with different impact value
