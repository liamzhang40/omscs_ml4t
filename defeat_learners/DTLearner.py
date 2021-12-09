""""""
"""  		  	   		   	 		  		  		    	 		 		   		 		  
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		   	 		  		  		    	 		 		   		 		  
Note, this is NOT a correct DTLearner; Replace with your own implementation.  		  	   		   	 		  		  		    	 		 		   		 		  
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
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: lzhang699 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 903658227 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""




import numpy as np
class DTLearner(object):
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    This is a decision tree learner object that is implemented incorrectly. You should replace this DTLearner with  		  	   		   	 		  		  		    	 		 		   		 		  
    your own correct DTLearner from Project 3.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param leaf_size: The maximum number of samples to be aggregated at a leaf, defaults to 1.  		  	   		   	 		  		  		    	 		 		   		 		  
    :type leaf_size: int  		  	   		   	 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		   	 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.  		  	   		   	 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		   	 		  		  		    	 		 		   		 		  
    """

    def __init__(self, leaf_size=1, verbose=False):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		   	 		  		  		    	 		 		   		 		  
        """
        self.leaf_size = leaf_size
        self.verbose = verbose

    def author(self):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        :return: The GT username of the student  		  	   		   	 		  		  		    	 		 		   		 		  
        :rtype: str  		  	   		   	 		  		  		    	 		 		   		 		  
        """
        return "lzhang699"  # replace tb34 with your Georgia Tech username

    def add_evidence(self, data_x, data_y):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Add training data to learner  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param data_x: A set of feature values used to train the learner  		  	   		   	 		  		  		    	 		 		   		 		  
        :type data_x: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        :param data_y: The value we are attempting to predict given the X data  		  	   		   	 		  		  		    	 		 		   		 		  
        :type data_y: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        """

        data = np.concatenate((data_x, data_y[np.newaxis].T), axis=1)
        self.tree = self.build_tree(data)
        if self.verbose:
            print("Tree built successfully\n{}".format(self.tree))

    def query(self, points):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Estimate a set of test points given the model we built.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		   	 		  		  		    	 		 		   		 		  
        :type points: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        :return: The predicted result of the input data according to the trained model  		  	   		   	 		  		  		    	 		 		   		 		  
        :rtype: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        """
        y_predict = np.empty(points.shape[0])

        for idx, x in enumerate(points):
          # start from the root
          node_idx = 0
          # until a leaf is reached
          while self.tree[node_idx, 0] != -1:
            node = self.tree[node_idx]
            factor_idx, split_val, left_child, right_child = node

            if x[int(factor_idx)] <= split_val:
              node_idx += int(left_child)
            else:
              node_idx += int(right_child)

          y_predict[idx] = self.tree[node_idx, 1]

        return y_predict

    def build_tree(self, data):
        # if there is only one row left
        # or if all y labels are the same, then there is no point recursing
        if data.shape[0] == 1 or np.all(data[:, -1] == data[0, -1]):
          return np.array([[-1, data[0, -1], -1, -1]])

        if self.leaf_size and data.shape[0] <= self.leaf_size:
          y_mean = np.mean(data[:, -1])
          return np.array([[-1, y_mean, -1, -1]])

        feature_idx = self.find_feature_idx(data)

        if feature_idx == np.nan:
          # edge case: all feature corr is nan
          # temp solution: take y mean
          y_mean = np.mean(data[:, -1])
          return np.array([[-1, y_mean, -1, -1]])

        feature_col = data[:, feature_idx]
        split_val = np.median(feature_col)
        left_tree_data = data[feature_col <= split_val]
        right_tree_data = data[feature_col > split_val]

        if left_tree_data.shape[0] == 0 or right_tree_data.shape[0] == 0:
          split_val = np.mean(feature_col)
          left_tree_data = data[feature_col <= split_val]
          right_tree_data = data[feature_col > split_val]

        left_tree = self.build_tree(left_tree_data)
        right_tree = self.build_tree(right_tree_data)
        root = np.array([[feature_idx, split_val, 1, left_tree.shape[0] + 1]])

        return np.concatenate((root, left_tree, right_tree))

    def find_feature_idx(self, data):
        # this throws a RuntimeWarning if feature STD is zero
        corr = np.corrcoef(data[:, :-1].T, data[:, -1])[-1, :-1]
        # ignore features with no correlation, np.nan
        # edge case: all feature corr is nan
        try:
          idx = np.nanargmax(np.absolute(corr))
        except ValueError as e:
          print(e, 'all features have zero STDs')
          return np.nan

        return idx
