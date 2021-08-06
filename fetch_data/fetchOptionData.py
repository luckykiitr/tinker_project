import os
import pandas as pd
import datetime as dt
import sqlalchemy
import logging

logging.basicConfig(level=logging.INFO)


class FetchOptionData:
    """Only For 2021 data folder"""
    """
    1. pass path
    2. then set exp"""
    """
    path = r'F:\\Database\\Drive Data\\weekly option\\Nifty\\2021'
    fetch_data_obj = FetchData(path)
    fetch_data_obj.set_expiry(dt.date(2021, 4, 1))
    df = fetch_data_obj.get_data(15000, "CE")"""

    def __init__(self, path):
        self.path = path
        self.inside_folder = None

    def set_expiry(self, exp):
        """Pass the Expiry Date in dt format"""
        str_dt = str(exp.day)
        if len(str_dt) == 1:
            str_dt = "0" + str_dt
        str_dt = str_dt + exp.strftime("%b").upper()
        self.inside_folder = os.path.join(self.path, str_dt)

    def get_data(self, strike, cepe):
        """pass the strike price and CE and PE"""
        file_path = os.path.join(self.inside_folder, str(strike) + cepe + ".csv")
        df = pd.read_csv(file_path, names=["symbol", "Date", "Time", "Open", "High", "Low", "Close", "Volume", "oi"])
        df['Date'] = pd.to_datetime(df['Date'])
        Time_list = [dt.datetime.combine(df['Date'][i].date(), dt.datetime.strptime(df['Time'][i], "%H:%M").time()) for
                     i in range(len(df))]
        df["Time"] = Time_list
        df = df[["Time", "Open", "High", "Low", "Close", "Volume", "oi"]].copy()
        df.set_index("Time", inplace=True)
        return df


class IndexData:
    """Get data from local data base NIFTY database
        path = F:\\DB_database\\index_data"""
    """
    1. by default symbol is set to NIFTY
    2. to change it .. either initialize it or use method - change)symbol
    """

    def __init__(self, symbol="NIFTY"):
        self.engine = sqlalchemy.create_engine(f'sqlite:///F:/DB_database/{symbol}.db')
        self.symbol = symbol

    def change_symbol(self, symbol):
        logging.info(f"Change Symbol to {symbol}")
        self.engine = sqlalchemy.create_engine(f'sqlite:///F:/DB_database/{symbol}.db')
        self.symbol = symbol

    def fetch_data(self):
        logging.info(f"Retrieving Data ... {self.symbol}")
        df = pd.read_sql(f'SELECT * FROM {self.symbol}', self.engine)
        df['Datetime'] = pd.to_datetime(df["Datetime"])
        df.set_index("Datetime", inplace=True)
        return df




if __name__ == "__main__":
    pass
    # path = r"F:\Database\Drive Data\weekly option\Nifty\2021"
    # fetch_data_obj = FetchOptionData(path)
    # fetch_data_obj.set_expiry(dt.date(2021, 4, 1))
    # df = fetch_data_obj.get_data(15000, "CE")
    # print(df.tail())

