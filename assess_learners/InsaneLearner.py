from LinRegLearner import LinRegLearner
from BagLearner import BagLearner
import numpy as np
class InsaneLearner(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.learners = []
        for i in range(0, 20):
          self.learners.append(BagLearner(learner=LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False))
    def author(self):
        return "lzhang699"
    def add_evidence(self, x_train, y_train):
        for learner in self.learners:
          learner.add_evidence(x_train, y_train)
    def query(self, x_test):
        y_predict = np.zeros(x_test.shape[0])
        for learner in self.learners:
          y_predict += learner.query(x_test)
        return y_predict / x_test.shape[0]