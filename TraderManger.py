import pandas as pd

from model.Option_data_model import OptionFeed
import datetime as dt
from model.Position import Position


class TradeManager:
    path = r"F:\Database\Drive Data\weekly option\Nifty\2021"

    def __init__(self, expiry):
        self.positions = []
        self.expiry = expiry
        self.option_feed = OptionFeed(TradeManager.path, self.expiry)

    def create_pos(self, strike, dt_time, cepe, qty):
        """Pass qty with sign"""
        symbol = str(strike) + cepe
        data = self.option_feed.get_feed(strike, cepe, dt_time)
        pos = Position(symbol, strike, cepe, self.expiry)
        pos.set_qty(qty)
        if qty > 0:
            pos.set_bp(data['Close'])
        elif qty < 0:
            pos.set_sp(data['Close'])
        self.positions.append(pos)

    def close(self, strike, dt_time, cepe):
        for pos in self.positions:
            if strike == pos.strike and not pos.booked:
                data = self.option_feed.get_feed(strike, cepe, dt_time)

                if pos.qty > 0:
                    pos.sp = data['Close']
                elif pos.qty < 0:
                    pos.bp = data['Close']

                pos.booked = True
                pos.calculate_pnl()
                break

    def square_off_all(self, dt_time):
        for pos in self.positions:
            if not pos.booked:
                data = self.option_feed.get_feed(pos.strike, pos.cepe, dt_time)

                if pos.qty > 0:
                    pos.sp = data['Close']
                elif pos.qty < 0:
                    pos.bp = data['Close']
                pos.booked = True
                pos.calculate_pnl()

    def get_total_mtm(self, dt_time):
        total_mtm = 0
        for pos in self.positions:
            if not pos.booked:
                data = self.option_feed.get_feed(pos.strike, pos.cepe, dt_time)
                total_mtm = total_mtm + pos.get_mtm(dt_time)
            else:
                total_mtm = total_mtm + pos.get_pnl()
        return total_mtm

    def all_positions(self, dt_time):
        df = pd.DataFrame()
        for pos in self.positions:
            data = self.option_feed.get_feed(pos.strike, pos.cepe, dt_time)
            if not pos.booked:
                df = pd.concat([df, pd.DataFrame({"symbol": [pos.symbol], "qty": [pos.qty], "Avg_Price":[pos.bp if pos.qty>0 else pos.sp], "mtm": pos.get_mtm(dt_time), "LTP":data['Close']})])
            else:
                df = pd.concat([df, pd.DataFrame({"symbol": [pos.symbol], "qty": [0.0], "Avg_Price":[pos.bp if pos.qty>0 else pos.sp], "mtm": pos.get_pnl(), "LTP":data['Close']})])
            df.set_index(pd.Series(list(range(1, len(df)+1))), inplace=True)
        return df
