""""""
"""  		  	   		   	 		  		  		    	 		 		   		 		  
A simple wrapper for Decision Tree learner		  	   		   	 		  		  		    	 		 		   		 		  
"""


import numpy as np
np.seterr(divide='ignore', invalid='ignore')


class DTLearner(object):
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    This is a Linear Regression Learner. It is implemented correctly.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		   	 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.  		  	   		   	 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		   	 		  		  		    	 		 		   		 		  
    """

    def __init__(self, leaf_size=False, verbose=False):
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
        return "lzhang699"

    def add_evidence(self, x_train, y_train):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Add training data to learner  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param x_train: A set of feature values used to train the learner  		  	   		   	 		  		  		    	 		 		   		 		  
        :type x_train: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        :param y_train: The value we are attempting to predict given the X data  		  	   		   	 		  		  		    	 		 		   		 		  
        :type y_train: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        """

        data = np.concatenate((x_train, y_train[np.newaxis].T), axis=1)
        self.tree = self.build_tree(data)
        if self.verbose:
            print("Tree built successfully\n{}".format(self.tree))

    def query(self, x_test):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Estimate a set of test points given the model we built.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		   	 		  		  		    	 		 		   		 		  
        :type points: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        :return: The predicted result of the input data according to the trained model  		  	   		   	 		  		  		    	 		 		   		 		  
        :rtype: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        """
        y_predict = np.empty(x_test.shape[0])

        for idx, x in enumerate(x_test):
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
