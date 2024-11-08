import pandas as pd
from Organizer import Manager
import Helper

class Preprocessor():
    def __init__(self, manager: Manager, threshold: float = 0.5):
        self._threshold = threshold
        self.manager = manager
        print("Preprocessor is ready!")

    def analyseBenchmark(self, table:str = "index_fund") -> True:
        rows = self.manager._datasource.readData("index_fund", cols = list(['symbol', 'weight']), where= list([('name', self.manager._benchmark), ('date', Helper.currentDate())]), sortBy='weight')
        dfAstWeights = pd.DataFrame(rows, columns=['symbol', 'weight'])
        dfAstWeights['cweight'] = dfAstWeights['weight'].cumsum()
        print(dfAstWeights.head())
        dfSubAsts = dfAstWeights[dfAstWeights['cweight'] <= self._threshold]
        dfSubAsts = dfSubAsts.drop(columns=['cweight'])
        # self.dataSource.updateFilter(dfSubAsts, self.benchMark)
        self.manager._datasource.updateFilter(dfSubAsts[:10], self.manager._benchmark)
        return True
    
    def updateTimeSeries(self) -> True:
        rows = self.manager._datasource.readData("assets_indexfund", cols = list(['symbol']), where= list([('name', self.manager._benchmark), ('date', Helper.currentDate())]), sortBy='weight')
        symbols = pd.DataFrame(rows, columns=['symbol'])
        self.manager._datasource.updateTimeSeries('SPY')
        symbols['symbol'].apply(
            lambda x: self.manager._datasource.updateTimeSeries(x)
        )        
        return True
    
    def visualize(self):
        rows = self.manager._datasource.readData("assets_indexfund", cols = list(['symbol']), where= list([('name', self.manager._benchmark), ('date', Helper.currentDate())]), sortBy='weight')
        symbols = pd.DataFrame(rows, columns=['symbol'])
        table = Helper.simpleString(self.manager._benchmark)
        data = self.manager._datasource.getTimeSeries(self.manager._benchmark)
        print(data.head())
        # self.plotTimeSeries(data, title=table)
        self.manager._visualizer.plotCandleSticks(data, title=table)
        for sym in symbols['symbol'][:10]:
            self.manager._visualizer.plotTimeSeries(self.manager._datasource.getTimeSeries(sym), title=sym)
    
    def kickoff(self) -> None:
        self.analyseBenchmark()
        self.updateTimeSeries()
        self.visualize()
        return
