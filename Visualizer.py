import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

class Visualizer():
    def __init__(self):
        print("Visualizer is running!")

    def plotTimeSeries(self, data: pd.DataFrame, title: str = 'Unspecified') -> None:
        if(data is None):
            return
        plt.plot(data.date, data['close'], label=title)
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Time Series Data of ' + title)
        plt.legend()
        plt.show()
        return

    def plotCandleSticks(self, data: pd.DataFrame, title: str = 'Unspecified') -> None:
        if(data is None):
            return
        data = data.set_index('date')
        mpf.plot(data, type='candle', style='charles', title='Candle Stick Chart of ' + title, ylabel='Value')
        plt.show()

    def quickPlot(self, data: pd.Series, title: str = 'Unspecified'):
        plt.plot(data)
        plt.title(title)
        plt.show()    

    def multiPlot(self, data: pd.DataFrame, title: str = 'Unspecified'):
        data.plot()
        plt.title(title)
        plt.show()
