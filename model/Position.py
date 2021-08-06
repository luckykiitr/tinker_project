from model.Option_data_model import OptionFeed


class Position:
    """ create this position and dont try to modify.. it is just simple make and close kind of thing"""

    def __init__(self, symbol, strike, cepe, expiry):
        self.strike = strike
        self.cepe = cepe
        self.symbol = symbol
        self.sp = None
        self.bp = None
        self.qty = None
        self.pnl = None
        self.booked = False
        self.expiry = expiry

    def set_bp(self, bp):
        self.bp = bp

    def set_sp(self, sp):
        self.sp = sp

    def set_qty(self, qty):
        self.qty = qty

    def get_mtm(self, dt_time):
        path = r"F:\Database\Drive Data\weekly option\Nifty\2021"
        option_feed = OptionFeed(path, self.expiry)
        data = option_feed.get_feed(self.strike, self.cepe, dt_time)
        # print(data)
        if self.qty > 0:
            return (data['Close'] - self.bp)*self.qty
        elif self.qty < 0:
            return (self.sp - data['Close'])*abs(self.qty)

    def calculate_pnl(self):
        self.pnl = (self.sp - self.bp) * abs(self.qty)

    def get_pnl(self):
        return self.pnl

    def set_booked(self):
        self.booked = True


