from DataSource import Datasource
from Visualizer import Visualizer

class Manager:
    def __init__(self, API: str = "AV", benchMark: str = "SPY"):
        self._API = API
        self._benchmark = benchMark
        self._datasource = Datasource(API=self._API)
        self._visualizer = Visualizer()
        print("Manager is ready!")

    def kickoff(self) -> None:
        self._datasource.updateBenchmark()