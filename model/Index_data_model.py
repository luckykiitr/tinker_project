import pandas as pd
import logging
from fetch_data.fetchOptionData import IndexData
import datetime as dt


# create different objects for Index option class
class Index:
    DATA = pd.DataFrame()

    def __init__(self, symbol="NIFTY"):
        index_data = IndexData(symbol)
        self.symbol = symbol
        Index.DATA = index_data.fetch_data()

    def get_data(self, fro, to):
        logging.info(f"Data for {self.symbol} to : {to}   from : {fro}")
        data = Index.DATA[Index.DATA.index >= fro].copy()
        data = data[data.index <= to].copy()
        return data
