import os
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import requests
import pandas as pd

class AlphaVantage:
    def __init__(self):
        self.value = os.getenv(key="ALPHAVANTAGE_API_KEY")
        self.RESTApi = {
            "URL": "https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}"
        }
        self.params = {
            "function": None,
            "symbol": None,
            "apikey": self.value,
        }

        self.endPOints = {
            "functions" :{
                "Timseries":{
                    "daily": None
                }
            },
            "symbols": {

            }
        }
        print("AlphaVantage object created")

    def getURLResponse(self, function , symbol) -> pd.DataFrame:
        try:
            self.params["function"] = function
            self.params["symbol"] = symbol
            url = self.RESTApi["URL"].format(**self.params)
            response = requests.get(url)
            if response.status_code != 200 or "Error Message" in response.text:
                print(f"Error: {response.status_code}")
                return None
            data = response.json()
            print("Data received")
            return data
        except Exception as e:
            print(f"Error: {e}")
            return None

    def getPortfoliio(self) -> pd.DataFrame:
        pass
