""""""
"""  		  	   		   	 		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
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
"""


import sys
import time
from RTLearner import RTLearner
import numpy as np
import matplotlib.pyplot as plt
from InsaneLearner import InsaneLearner
from DTLearner import DTLearner
from BagLearner import BagLearner
import LinRegLearner as lrl
import math
if __name__ == "__main__":
    print(time.time())
    if len(sys.argv) != 2:
        print("Usage: python testlearner.py <filename>")
        sys.exit(1)

    datafile = sys.argv[1]
    inf = open(datafile)
    data = np.genfromtxt(inf, delimiter=",")
    # Skip the date column and header row if we're working on Istanbul data
    if datafile == "Data/Istanbul.csv":
        data = data[1:, 1:]

    def find_rmse(pred, actu):
        return math.sqrt(
            ((actu - pred) ** 2).sum() / actu.shape[0])

    def find_train_and_test(data):
        # compute how much of the data is training and testing
        train_rows = int(0.6 * data.shape[0])

        # separate out training and testing data
        train_x = data[:train_rows, 0:-1]
        train_y = data[:train_rows, -1]
        test_x = data[train_rows:, 0:-1]
        test_y = data[train_rows:, -1]

        return train_x, train_y, test_x, test_y

    def execute_learner(LearnerClass, data, total_leaf, times, func):
        time_to_build = np.zeros(total_leaf)
        y_in_sample = np.zeros(total_leaf)
        y_out_sample = np.zeros(total_leaf)
        data_copy = np.ndarray.copy(data)
        for i in range(times):
            train_x, train_y, test_x, test_y = find_train_and_test(data_copy)

            y_in_sample_temp = []
            y_out_sample_temp = []
            time_to_build_temp = []

            for size in range(total_leaf):
                start_time = time.time()
                learner = LearnerClass(leaf_size=size + 1)
                learner.add_evidence(train_x, train_y)
                end_time = time.time()

                time_to_build_temp.append(end_time - start_time)

                pred_y = learner.query(train_x)
                metric = func(pred_y, train_y)
                y_in_sample_temp.append(metric)

                pred_y = learner.query(test_x)
                metric = func(pred_y, test_y)
                y_out_sample_temp.append(metric)

            np.random.shuffle(data_copy)
            time_to_build += time_to_build_temp
            y_in_sample += y_in_sample_temp
            y_out_sample += y_out_sample_temp

        return y_in_sample / times, y_out_sample / times, time_to_build

    def execute_bag_learner(LearnerClass, bags, data, total_leaf, times, func):
        time_to_build = np.zeros(total_leaf)
        y_in_sample = np.zeros(total_leaf)
        y_out_sample = np.zeros(total_leaf)
        data_copy = np.ndarray.copy(data)
        for i in range(times):
            train_x, train_y, test_x, test_y = find_train_and_test(data_copy)

            y_in_sample_temp = []
            y_out_sample_temp = []
            time_to_build_temp = []
            for size in range(total_leaf):
                start_time = time.time()
                learner = BagLearner(
                    LearnerClass, {"leaf_size": size + 1}, bags=bags)
                learner.add_evidence(train_x, train_y)
                end_time = time.time()

                time_to_build_temp.append(end_time - start_time)

                pred_y = learner.query(train_x)
                metric = func(pred_y, train_y)
                y_in_sample_temp.append(metric)

                pred_y = learner.query(test_x)
                metric = func(pred_y, test_y)
                y_out_sample_temp.append(metric)

            np.random.shuffle(data_copy)
            time_to_build += time_to_build_temp
            y_in_sample += y_in_sample_temp
            y_out_sample += y_out_sample_temp

        return y_in_sample / times, y_out_sample / times, time_to_build

    def test_code(seed, data):
        np.random.seed(seed)
        np.random.shuffle(data)

    total_leaf = 50
    x = np.arange(1, total_leaf + 1)




    # Experiment 1
    times = 1

    y_in_sample, y_out_sample, _ = execute_learner(
        DTLearner, data=data, total_leaf=total_leaf, times=times, func=find_rmse)
    plt.plot(x, y_in_sample, label='In sample results')
    plt.plot(x, y_out_sample, label='Out of sample results')
    plt.title('Experiment 1 DTLearner')
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.xlim(left=0)
    plt.ylim()
    plt.legend(loc='lower right')
    # plt.show()
    # plt.savefig('experiment_1_{}_times_avg.png'.format(times))
    plt.close()

    # Similar to bagging, basically sampling without replacement
    times = 10
    y_in_sample, y_out_sample, _ = execute_learner(
        DTLearner, data=data, total_leaf=total_leaf, times=times, func=find_rmse)
    plt.plot(x, y_in_sample, label='In sample results')
    plt.plot(x, y_out_sample, label='Out of sample results')
    plt.title('Experiment 1 DTLearner {} Time(s) Avg'.format(times))
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.xlim(left=0)
    plt.ylim()
    plt.legend(loc='lower right')
    # plt.show()
    # plt.savefig('experiment_1_{}_times_avg.png'.format(times))
    plt.close()




    # Experiment 2
    bags = 20
    times = 10
    y_in_sample, y_out_sample, _ = execute_bag_learner(
        DTLearner ,bags=bags, data=data, total_leaf=total_leaf, times=times, func=find_rmse)

    plt.plot(x, y_in_sample, label='In sample results')
    plt.plot(x, y_out_sample, label='Out of sample results')
    plt.title(
        'Experiment 2 BagLearner w/ {} DTLearner(s) {} Time(s) Avg'.format(bags, times))
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.xlim(left=0)
    plt.ylim()
    plt.legend(loc='lower right')
    # plt.show()
    # plt.savefig('experiment_2_{}_times_avg.png'.format(times))
    plt.close()




    # Experiment 3
    gtid = 903658227
    data_copy = np.ndarray.copy(data)
    times = 10
    test_code(gtid, data_copy)

    def find_mae(pred, actu):
        return np.absolute(actu - pred).sum() / actu.shape[0]

    y_in_sample, y_out_sample, time_to_build_d = execute_learner(
        DTLearner, data=data, total_leaf=total_leaf, times=times, func=find_mae)
    plt.plot(x, y_in_sample, label='DTL In sample results')
    plt.plot(x, y_out_sample, label='DTL Out of sample results')
    # plt.show()

    y_in_sample, y_out_sample, time_to_build_r = execute_learner(
        RTLearner, data=data, total_leaf=total_leaf, times=times, func=find_mae)
    plt.plot(x, y_in_sample, label='RTL In sample results')
    plt.plot(x, y_out_sample, label='RTL Out of sample results')
    plt.title('Experiment 3 DTLearner vs RTLearner {} Time(s) Avg'.format(times))
    plt.xlabel("Leaf Size")
    plt.ylabel("MAE")
    plt.xlim(left=0)
    plt.ylim()
    plt.legend(loc='lower right')
    # plt.savefig('experiment_3_dtl_vs_rtl_mae_{}_times_avg.png'.format(times))
    plt.close()

    plt.plot(x, time_to_build_d, label='DTLearner')
    plt.plot(x, time_to_build_r, label='RTLearner')
    plt.title('Experiment 3 Time To Build {} Time(s) Avg'.format(times))
    plt.xlabel("Leaf Size")
    plt.ylabel("Time(s)")
    plt.xlim(left=0)
    plt.ylim()
    plt.legend(loc='upper right')
    # plt.show()
    # plt.savefig('experiment_3_time_to_build_{}_times_avg.png'.format(times))
    plt.close()

    # correlation_matrix = np.corrcoef(y_in_sample, y_out_sample)
    # correlation_xy = correlation_matrix[0, 1]
    # print(correlation_xy**2)

    dtl_bags = 10
    times = 30
    y_in_sample, y_out_sample, time_to_build_d = execute_bag_learner(
        DTLearner, bags=dtl_bags, data=data, total_leaf=total_leaf, times=times, func=find_mae)

    plt.plot(x, y_out_sample, label='{} Bagged DTL Out of sample results'.format(dtl_bags))
    # plt.show()

    rtl_bags = dtl_bags * 3
    y_in_sample, y_out_sample, time_to_build_r = execute_bag_learner(
        RTLearner, bags=rtl_bags, data=data, total_leaf=total_leaf, times=times, func=find_mae)

    plt.plot(x, y_out_sample, label='{} Bagged RTL Out of sample results'.format(rtl_bags))
    plt.title(
        'Experiment 3 BagLearner w/ DTLearners(s) vs. RTLearner(s) {} Time(s) Avg'.format(rtl_bags, times))
    plt.xlabel("Leaf Size")
    plt.ylabel("MAE")
    plt.xlim(left=0)
    plt.ylim()
    plt.legend(loc='lower right')
    # plt.show()
    # plt.savefig('experiment_3_bagged_dtl_vs_rtl_{}_times_avg.png'.format(times))
    plt.close()

    plt.plot(x, time_to_build_d, label='{} Bagged DTLearner'.format(dtl_bags))
    plt.plot(x, time_to_build_r, label='{} Bagged RTLearner'.format(rtl_bags))
    plt.title('Experiment 3 Time To Build BagLearner {} Time(s) Avg'.format(times))
    plt.xlabel("Leaf Size")
    plt.ylabel("Time(s)")
    plt.xlim(left=0)
    plt.ylim()
    plt.legend(loc='upper right')
    # plt.show()
    # plt.savefig('experiment_3_bagged_time_to_build_{}_times_avg.png'.format(times))
    plt.close()
    print(time.time())
