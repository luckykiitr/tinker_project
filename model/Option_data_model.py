from fetch_data.fetchOptionData import FetchOptionData
import datetime as dt
import logging


# create different objects for Index option class
class IndexOption:
    def __init__(self, path, expiry, strike, cepe):
        fetch_data = FetchOptionData(path)
        fetch_data.set_expiry(expiry)
        self.df = fetch_data.get_data(strike, cepe)
        self.fetch_data = fetch_data


# feed by time
class OptionFeed:
    """create only one function and get feed by passing time and strike price"""
    """path = r"F:\\Database\\Drive Data\\weekly option\\Nifty\\2021"
    option_feed = OptionFeed(path, dt.datetime(2021, 4, 1))
    data = option_feed.get_feed(15300, "PE", dt.datetime(2021, 4, 1, 9, 30))
    data will be in dict format"""
    
    fetch_data = None
    data = {}

    def __init__(self, path, expiry):
        self.path = path
        fetch_data = FetchOptionData(path)
        fetch_data.set_expiry(expiry)
        OptionFeed.fetch_data = fetch_data

    @staticmethod
    def get_feed(strike, cepe, dt_time):
        symbol = str(strike) + cepe
        if symbol not in OptionFeed.data.keys():
            OptionFeed.data[symbol] = OptionFeed.fetch_data.get_data(strike, cepe)
        df = OptionFeed.data[symbol]
        df = df[df.index == dt_time].copy()
        if df.empty:
            logging.info("No data... Error from get_feed method")
            raise KeyError
        return df.to_dict('records')[-1]


if __name__ == "__main__":
    path = r"F:\Database\Drive Data\weekly option\Nifty\2021"
    option_feed = OptionFeed(path, dt.datetime(2021, 4, 1))
    data = option_feed.get_feed(14100, "PE", dt.datetime(2021, 1, 5, 9, 21))
