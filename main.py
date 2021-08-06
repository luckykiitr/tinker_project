from model.Option_data_model import OptionFeed
from TraderManger import TradeManager
from model.Index_data_model import Index
import datetime as dt
from datetime import timedelta
from tkcalendar import Calendar
from tkinter import *
import tkinter as tk
from tkinter import ttk
import logging
logging.basicConfig(level=logging.INFO)

# Create Object
root = tk.Tk()

# Set geometry
# root.geometry("800x600")


class Calen:
    FROM_ = None
    To_ = None
    EXP = None
    TRADE_DAY = None

    def __init__(self, root):
        self.root = root

        # frame
        self.cal_frame = ttk.LabelFrame(self.root, text="Calender")
        self.cal_frame.grid(row=1, column=0)
        
        self.button_frame = ttk.LabelFrame(self.root, text="Buttons")
        self.button_frame.grid(row=1, column=1)

        # Display Date frame
        self.selected_date = ttk.LabelFrame(self.root, text="Selected Dates")
        self.selected_date.grid(row=1, column=2, sticky=tk.N)

        # display
        self.cal = Calendar(self.cal_frame, selectmode = 'day', year = 2021, month = 1, day = 1)
        self.cal.grid(row=0, column=0)

        # create label
        self.expiry_display_label = ttk.Label(self.selected_date, text = "Expiry Date : ")
        self.from_display_label = ttk.Label(self.selected_date, text =   "From Date  : ")
        self.to_display_label = ttk.Label(self.selected_date, text =     "To Date       : ")

        # display label
        self.expiry_display_label.grid(row=0, column=0, sticky=tk.W)
        self.from_display_label.grid(row=1, column=0, sticky=tk.W)
        self.to_display_label.grid(row=2, column=0, sticky=tk.W)

        # Add Button
        ttk.Button(self.button_frame, text = "Set Expiry", command = self.set_expiry, width=20).grid(row=0, column=1)
        ttk.Button(self.button_frame, text = "Set From Date", command = self.set_from, width=20).grid(row=1, column=1)
        ttk.Button(self.button_frame, text = "Set To Date", command = self.set_to, width=20).grid(row=2, column=1)
        ttk.Button(self.button_frame, text = "Get Date", command = self.grad_date, width=20).grid(row=3, column=1)

    def grad_date(self):
        dt_time = dt.datetime.strptime(self.cal.get_date(), "%m/%d/%y")
        print(dt_time)

    def set_from(self):
        Calen.FROM_ = dt.datetime.strptime(self.cal.get_date(), "%m/%d/%y")
        self.from_display_label.config(text = f"From Date  : {Calen.FROM_.date()}")

    def set_to(self):
        Calen.To_ = dt.datetime.strptime(self.cal.get_date(), "%m/%d/%y")
        self.to_display_label.config(text = f"To Date       : {Calen.To_.date()}")

    def set_expiry(self):
        Calen.EXP = dt.datetime.strptime(self.cal.get_date(), "%m/%d/%y")
        self.expiry_display_label.config(text = f"Expiry Date : {Calen.EXP.date()}")
        Calen.TRADE_DAY = Calen.EXP - timedelta(days=9)
        ttk.Label(self.selected_date, text = f"Trade Execution Date: {Calen.TRADE_DAY.date()}").grid(row=3, column=0)


class Controller:

    def __init__(self, root):
        self.root = root
        self.calen = Calen(self.root)
        self.df = None
        self.msg = Label(root, text="", font=("Arial", 18), fg="red")
        self.msg.grid(row = 0, column=0)
        self.i = 0
        self.Index_data_obj = None
        self.buttons()

        # option label
        Label(self.root, width=12, text="NIFTY ATM").grid(row=2, column=1)
        Label(self.root, width=12, text="CE").grid(row=2, column=2)
        Label(self.root, width=12, text="PE").grid(row=2, column=3)

        # options cepe display
        self.nifty_atm_display = Entry(self.root, width=12, fg="blue", font=('Arial',16))
        self.nifty_atm_display.grid(row=3, column=1)
        self.ce_display = Entry(self.root, width=12, fg="blue", font=('Arial',16))
        self.ce_display.grid(row=3, column=2)
        self.pe_display = Entry(self.root, width=12, fg="blue", font=('Arial',16))
        self.pe_display.grid(row=3, column=3)

        # Display LTP of CE PE
        self.dt_time = Entry(self.root, width=19, fg="blue", font=('Arial',16))
        self.dt_time.grid(row=4, column=1)

        self.ltp_ce = Entry(self.root, width=12, fg="blue", font=('Arial',16))
        self.ltp_ce.grid(row=4, column=2)
        self.ltp_pe = Entry(self.root, width=12, fg="blue", font=('Arial',16))
        self.ltp_pe.grid(row=4, column=3)

        # simple
        Label(self.root, width=12, text="Date").grid(row=5, column=1)
        Label(self.root, width=12, text="LTP").grid(row=5, column=2)
        Label(self.root, width=12, text="LTP").grid(row=5, column=3)
        Label(self.root, width=12, text="Create Position", font=("Arial", 15), fg="red").grid(row=7, column=0)

        # buy sell combobox
        vals = ["CE", "PE"]
        self.var = tk.StringVar()
        self.cepe_combo = ttk.Combobox(self.root, width=14, textvariable=self.var, state="readonly")
        self.cepe_combo['values'] = vals
        self.cepe_combo.grid(rows=8, column=1)

        Label(self.root, width=12, text="QTY", font=("Arial", 13)).grid(row=8, column=2)
        self.qty = Entry(self.root, width=12, fg="blue", font=('Arial',13))
        self.qty.grid(row=8, column=3)



    def buttons(self):
        ttk.Button(self.root, text = "Fetch NIFTY data", command = self.fetch_index_data, width=25).grid(row=1, column=3)
        ttk.Button(self.root, text = "Auto Select CE & PE", command = self.choose_cepe, width=25).grid(row=2, column=0)
        ttk.Button(self.root, text = "i-=1", command = self.de_i_by_1, width=15).grid(row=6, column=0)
        ttk.Button(self.root, text = "i+=1", command = self.in_i_by_1, width=15).grid(row=6, column=1)
        ttk.Button(self.root, text = "i+=5", command = self.in_i_by_5, width=15).grid(row=6, column=2)
        ttk.Button(self.root, text = "i+=10", command = self.in_i_by_10, width=15).grid(row=6, column=3)
        ttk.Button(self.root, text = "Update LTP", command = self.update_ltp, width=15).grid(row=6, column=4)

        Button(self.root, text = "BUY", command = lambda : self.create_position("BUY"), width=15, bg='green').grid(row=8, column=4)
        Button(self.root, text = "SELL", command = lambda : self.create_position("SELL"), width=15, bg='red').grid(row=8, column=5)

    def update_ltp(self):
        if self.df is None:
            self.msg.config(text="First Fetch Nifty Data")
            return None
    
        self.ltp_ce.delete(0, tk.END)
        self.ltp_pe.delete(0, tk.END)

        self.ltp_ce.insert(tk.END, self.option_feeder.get_feed(self.ce_display.get(), "CE", self.df.index[self.i])['Close'])
        self.ltp_pe.insert(tk.END, self.option_feeder.get_feed(self.pe_display.get(), "PE", self.df.index[self.i])['Close'])
        self.CE = self.ce_display.get()
        self.PE = self.pe_display.get()

    def show_cepe(self):
        self.nifty_atm_display.delete(0, tk.END)
        self.nifty_atm_display.insert(tk.END, self.df.loc[self.df.index[self.i], "Close"])
    
    def choose_cepe(self):
        if self.df is None:
            self.msg.config(text="First Fetch Nifty Data")
            return None
        nifty_atm = self.df.loc[self.df.index[self.i], "Close"]
        self.nifty_atm = round(nifty_atm/50)*50
        self.CE = self.nifty_atm + 200
        self.PE = self.nifty_atm - 200

        self.ce_display.delete(0, tk.END)
        self.pe_display.delete(0, tk.END)
        self.ce_display.insert(tk.END, self.CE)
        self.pe_display.insert(tk.END, self.PE)
        self.show_cepe()

    def fetch_index_data(self):
        self.i = 0
        if (Calen.FROM_ is None) or (Calen.To_ is None):
            self.msg.config(text="Select Date First")
        else:
            if self.Index_data_obj is None:
                self.Index_data_obj = Index()
            self.df = self.Index_data_obj.get_data(Calen.FROM_, Calen.To_)
            self.msg.config(text="NIFTY Data Fetched")
            # This will get u trading day index
            for i in range(len(self.df)):
                if Calen.TRADE_DAY.date() == self.df.index[i].date():
                    if self.df.index[i].time() == dt.datetime(2020,2,2,15,20).time():
                        break

            # inside loop
            logging.info(f"Trading Date : {self.df.index[i]}")
            self.i = i
            self.trade_manager = TradeManager(expiry=Calen.EXP)
            self.option_feeder = OptionFeed(r"F:\\Database\\Drive Data\\weekly option\\Nifty\\2021", Calen.EXP)


    def in_i_by_1(self):
        self.i = self.i + 1    
        self.dt_time.delete(0, tk.END)
        self.dt_time.insert(tk.END, self.df.index[self.i])

        self.show_cepe()
        self.update_ltp()
        print(self.trade_manager.all_positions(self.df.index[self.i]))
        print(self.trade_manager.get_total_mtm(self.df.index[self.i]))
        
    def in_i_by_5(self):
        self.i = self.i + 5
        self.dt_time.delete(0, tk.END)
        self.dt_time.insert(tk.END, self.df.index[self.i])

        self.show_cepe()
        self.update_ltp()
        print(self.trade_manager.all_positions(self.df.index[self.i]))
        print(self.trade_manager.get_total_mtm(self.df.index[self.i]))

    def in_i_by_10(self):
        self.i = self.i + 10

        self.dt_time.delete(0, tk.END)
        self.dt_time.insert(tk.END, self.df.index[self.i])

        self.show_cepe()
        self.update_ltp()
        print(self.trade_manager.all_positions(self.df.index[self.i]))
        print(self.trade_manager.get_total_mtm(self.df.index[self.i]))

    def de_i_by_1(self):
        self.i = self.i - 1
        self.dt_time.delete(0, tk.END)
        self.dt_time.insert(tk.END, self.df.index[self.i])

        self.show_cepe()
        self.update_ltp()
        print(self.trade_manager.all_positions(self.df.index[self.i]))
        print(self.trade_manager.get_total_mtm(self.df.index[self.i]))

    def create_position(self, side):
        if side=="BUY":
            self.trade_manager.create_pos(self.CE if self.var.get() == "CE" else self.PE, self.df.index[self.i], self.var.get(), int(self.qty.get()))
        elif side=="SELL":
            self.trade_manager.create_pos(self.CE if self.var.get() == "CE" else self.PE, self.df.index[self.i], self.var.get(), int(self.qty.get())*-1)
        print(self.trade_manager.all_positions(self.df.index[self.i]))
        print(self.trade_manager.get_total_mtm(self.df.index[self.i]))

Controller(root)


# Excecute Tkinter
root.mainloop()



# nifty_val = df.loc[df.index[i], "Close"]

# trade_manager.create_pos(CE, df.index[i], "CE", -75)
# trade_manager.create_pos(PE, df.index[i], "PE", -75)

# # trade_manager.positions[0]

# try:
#     print(trade_manager.all_positions(df.index[i]))
#     print(trade_manager.get_total_mtm(df.index[i]))
#     print(df.index[i])
#     i = i + 1
# except:
#     print("No Feed")
#     print(df.index[i])
#     i = i + 1
