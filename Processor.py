import pandas as pd
from Organizer import Manager
from MeanReverting import MeanRevertion
from sklearn.preprocessing import MinMaxScaler

class Processor():
    def __init__(self, manager: Manager):
        self.manager = manager
        self.mr = MeanRevertion()
        print("Processor is ready!")

    def statisticalTest(self, data: pd.Series) -> bool:       
        staty = self.mr.testStaty(data)
        print(f'Stationarity: {staty}')

        th = self.mr.testThreshold(data)
        print(f'Threshold: {th}')

    def calcReturns(self, timeseries: pd.Series) -> pd.Series:
        returns =  timeseries.pct_change().dropna()
        print(returns.head())   
        print(returns.mean())
        print(self.mr.testStaty(returns))
        return returns
        
    def kickOff(self):
        data = self.manager._datasource.getTimeSeries('SPY')
        returns = self.calcReturns(data['close'])
        df = pd.DataFrame({'close': data['close'], 'returns': returns})
        df[['close', 'returns']] = MinMaxScaler().fit_transform(df[['close', 'returns']])
        self.manager._visualizer.multiPlot(df)
        # self.statisticalTest()    


    