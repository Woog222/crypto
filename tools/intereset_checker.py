import sys, os
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config.URL as URL
from tools.quotation_api import *

"""
chart columns
    'opening_price' : int(data['opening_price']),
    'trade_price' : int(data['trade_price']),
    'high_price' : int(data['high_price']),
    'low_price' : int(data['low_price']),
    'time_stamp' : int(data['timestamp']) / 1000,
    'acc_trade_price' : float(data['candle_acc_trade_price'])  
"""

class InterestChecker:

    def __init__(self, code:str, chart:pd.DataFrame):
        """
        :param code:
        :param chart: more than 97 hour candles
        """
        self.code = code
        self.chart = chart  # 60min(hour) chart are expected

        self.mean_price_48 = float(self.chart['trade_price'][1:49].mean())
        self.mean_price_96 = float(self.chart['trade_price'][1:97].mean())

        self.recent_volume = float(self.chart.loc[1, 'acc_trade_price'])
        self.max_volume_48 = float(self.chart['acc_trade_price'][1:49].max())

        self.max_price_48 = float(self.chart['trade_price'][1:49].max())
        self.prev_trade_price = int(self.chart.loc[1,'trade_price'])
        self.new_open_price = int(self.chart.loc[0, 'opening_price'])

    def is_hot(self):
        return self.was_bearish() and self.check_recent_volume_peak() and \
            self.check_price_peak() and self.check_price_jump()

    # 1. Was it a bearish trend?
    def was_bearish(self):
        return self.mean_price_48 < self.mean_price_96

    # 2. trade volume peak?
    def check_recent_volume_peak(self):
        return self.max_volume_48 <= self.recent_volume

    # 3. price peak?
    def check_price_peak(self):
        if self.max_price_48 <= float(self.prev_trade_price) and \
           float(self.chart.loc[2,'trade_price']) * 1.15 <= float(self.prev_trade_price):
            return True
        else: return False

    # 4. price jump?
    def check_price_jump(self):
        return self.prev_trade_price < self.new_open_price

    def __str__(self):
        sb = []
        sb.append(
            f"-------------{self.code} ({'YES' if self.is_hot() else 'NO'})--------------\n"
        )
        sb.append(
            f"1. was it a bearish trend? -> {self.was_bearish()} :\n\tavg_48_price({self.mean_price_48}), avg_96_price({self.mean_price_96})"
        )
        sb.append(
            f"2. trade volume peak? -> {self.check_recent_volume_peak()} :\n\tlast_volume({self.recent_volume}), max_48_volume({self.max_volume_48})"
        )
        sb.append(
            f"3. price_peak? -> {self.check_price_peak()} :\n\tlast_price({self.prev_trade_price}), max_48_price({self.max_price_48})"
        )
        sb.append(
            f"\t2 hours ago last price({float(self.chart.loc[2,'trade_price'])}) -> last_price({self.prev_trade_price})"
        )
        sb.append(
            f"4. price jump? -> {self.check_price_jump()} :\n\tlast_price({self.prev_trade_price}) -> new_open_price({self.new_open_price})\n"
        )

        return "\n".join(sb)

