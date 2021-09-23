""""""
"""  		  	   		   	 		  		  		    	 		 		   		 		  
A simple wrapper for Bag learner		  	   		   	 		  		  		    	 		 		   		 		  
"""




import numpy as np
class BagLearner(object):
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    This is a Linear Regression Learner. It is implemented correctly.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		   	 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.  		  	   		   	 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		   	 		  		  		    	 		 		   		 		  
    """

    def __init__(self, learner, kwargs, bags=1, boost=False, verbose=False):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		   	 		  		  		    	 		 		   		 		  
        """
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose

        self.init_learners()

    def author(self):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        :return: The GT username of the student  		  	   		   	 		  		  		    	 		 		   		 		  
        :rtype: str  		  	   		   	 		  		  		    	 		 		   		 		  
        """
        return "lzhang699"

    def init_learners(self):
        self.learners = []
        for i in range(0, self.bags):
          self.learners.append(self.learner(**self.kwargs))

    def add_evidence(self, x_train, y_train):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Add training data to learner  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param x_train: A set of feature values used to train the learner  		  	   		   	 		  		  		    	 		 		   		 		  
        :type x_train: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        :param y_train: The value we are attempting to predict given the X data  		  	   		   	 		  		  		    	 		 		   		 		  
        :type y_train: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        """

        data = np.concatenate((x_train, y_train[np.newaxis].T), axis=1)

        for learner in self.learners:
          sample = self.sample_with_replacement(data)
          learner.add_evidence(sample[:, :-1], sample[:, -1])

        if self.verbose:
            print("Forrest built successfully")

    def query(self, x_test):
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Estimate a set of test points given the model we built.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		   	 		  		  		    	 		 		   		 		  
        :type points: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        :return: The predicted result of the input data according to the trained model  		  	   		   	 		  		  		    	 		 		   		 		  
        :rtype: numpy.ndarray  		  	   		   	 		  		  		    	 		 		   		 		  
        """
        y_predict = np.zeros(x_test.shape[0])
        for learner in self.learners:
          y_predict += learner.query(x_test)

        return y_predict / self.bags

    def sample_with_replacement(self, data):
        sample = np.empty((data.shape[0], data.shape[1]), dtype=float)
        sample_idx = np.random.randint(data.shape[0], size=data.shape[0])
        for idx, el in enumerate(sample_idx):
          sample[idx] = data[el]

        return sample
