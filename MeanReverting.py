import numpy as np
from Strategy import Strategy
import pandas as pd
import statsmodels.tsa.stattools as stats
import scipy as sp
import matplotlib.pyplot as plt

class MeanRevertion(Strategy):
    def __init__(self, test='adf', threshold=0.05):
        self.test = test
        self.threshold = threshold
        print("Mean Revertion Strategy is called upon!")
    
    def testStaty(self, timeseries: pd.Series, threshold = None) -> bool:
        if(threshold is None):
            threshold = self.threshold
        if(self.test == 'adf'):
            result = stats.adfuller(timeseries, autolag='AIC')
            return result[1] <= threshold
        else:
            raise ValueError('Invalid test method')
        
    def testThreshold(self, timeseries: pd.Series) -> float:
        for t in np.arange(self.threshold, 0.01, -0.005):
            if(self.testStaty(timeseries, t)):
                return t  