import pandas as pd
from Database import Connection
import Config
import Helper

class Datasource:
    def __init__(self, API: str = "AV"):
        if(API == "AV"):
            from AlphaVantage import AlphaVantage
            self.api = AlphaVantage()
        print("Data object created") 
        self.conn = Connection(Config.db_config)
        print("Datasource is running!")
    
    def updateBenchmark(self, benchmark: str = "SPY") -> bool:
        data = self.api.getURLResponse(function="ETF_PROFILE", symbol = benchmark)
        if("holdings" not in data):
            print("No data returned for " + benchmark + "; skipping update")
            return False
        dfHoldings = pd.DataFrame(data["holdings"])        
        if(not self.conn.checkTable("index_fund")):            
            query ="""      
                date DATE NOT NULL,
                name VARCHAR(50) NOT NULL,
                symbol VARCHAR(10) NOT NULL,
                description TEXT,
                weight FLOAT NOT NULL,
                PRIMARY KEY (date, name, symbol)  -- Composite primary key
            """
            self.conn.createTable("index_fund", query)
        print("Table \"index_fund\" is ready!")
        date = Helper.currentDate()
        dfHoldings["date"] = date
        dfHoldings["name"] = benchmark
        dfHoldings = dfHoldings[["date", "name", "symbol", "description", "weight"]]
        self.conn.insertMany("index_fund", dfHoldings.columns, list(dfHoldings.itertuples(index=False, name=None)))
        print("Index Updated in database!")
        return True
    
    def updateFilter(self, data: pd.DataFrame, benchmark = "SPY") -> bool:
        if(not self.conn.checkTable("assets_indexfund")):            
            query ="""      
                date DATE NOT NULL,
                name VARCHAR(50) NOT NULL,
                symbol VARCHAR(10) NOT NULL,
                weight FLOAT NOT NULL,
                PRIMARY KEY (date, name, symbol)  -- Composite primary key
            """
            self.conn.createTable("assets_indexfund", query)
        print("Table \"assets_indexfund\" is ready!")
        date = Helper.currentDate()
        data["date"] = date
        data["name"] = benchmark
        data = data[["date", "name", "symbol", "weight"]]
        self.conn.insertMany("assets_indexfund", data.columns, list(data.itertuples(index=False, name=None)))
        print("Assets Updated in database!")
        return True

    def readData(self, table: str, cols: list = None, where: list[tuple] = None, sortBy: str = None, order='DESC') -> list:
        rows = self.conn.readTable(table, cols, where, sortBy, order)  
        return rows  
    
    def updateTimeSeries(self, symbol: str) -> bool:
        print("Updating Time Series for " + symbol)
        table = "time_series_" + Helper.simpleString(symbol)
        data = self.api.getURLResponse(function="TIME_SERIES_DAILY", symbol = symbol)
        if(data is None or "Time Series (Daily)" not in data):
            print("No data returned for " + symbol + "; skipping update")
            return False
        if(not self.conn.checkTable(table)):            
            query ="""      
                date DATE NOT NULL,
                symbol VARCHAR(10) NOT NULL,
                open FLOAT NOT NULL,
                high FLOAT NOT NULL,
                low FLOAT NOT NULL,
                close FLOAT NOT NULL,
                volume INT NOT NULL,
                PRIMARY KEY (date, symbol)  -- Composite primary key
            """
            self.conn.createTable(table, query)
        print("Table " + table + " is ready!")
        dfTimeSeries = pd.DataFrame(data["Time Series (Daily)"]).T
        dfTimeSeries["symbol"] = symbol
        dfTimeSeries = dfTimeSeries.reset_index()
        dfTimeSeries = dfTimeSeries.rename(columns={'index': 'date'})
        dfTimeSeries["date"] = pd.to_datetime(dfTimeSeries["date"])
        dfTimeSeries = dfTimeSeries[["date", "symbol", "1. open", "2. high", "3. low", "4. close", "5. volume"]]
        dfTimeSeries.columns = ["date", "symbol", "open", "high", "low", "close", "volume"]
        self.conn.insertMany(table, dfTimeSeries.columns, list(dfTimeSeries.itertuples(index=False, name=None)))
        print("Time Series Updated in database!")
        return True
    
    def getTimeSeries(self, symbol: str) -> pd.DataFrame:
        table = "time_series_" + Helper.simpleString(symbol)
        if(not self.conn.checkTable(table)):
            print("Table " + table + " does not exist!")
            return None
        print("Table " + table + " is ready!")
        rows = self.conn.readTable(table, cols = list(['date', 'open', 'high', 'low', 'close']), sortBy='date', order='ASC')
        dfTimeSeries = pd.DataFrame(rows, columns=['date', 'open', 'high', 'low', 'close'])
        dfTimeSeries['date'] = pd.to_datetime(dfTimeSeries['date'])
        return dfTimeSeries
    
    def addNInsert(self, table: str, col: str, dataType: str, data: pd.Series) -> None:
        self.conn.modifyTable(action=self.conn.modifyColumn['addColumn'], table=table, column=col, datatype=dataType)
        return
