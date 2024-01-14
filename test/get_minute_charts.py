import sys, os

from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools.quotation_api import *

count = 97
unit = 60


if __name__ == '__main__':

    codes = get_tickers()
    for code in tqdm(codes):
        chart = get_minute_charts(code=code, count=count, unit=unit)
        if chart is None: continue # http request issue

        if chart.shape[0] != 97 or chart.shape[1] != 6:
            print(f"{code} chart issue")
        if chart.isnull().any().any():
            print(f"{code} contains null value")




"""
Request Params (Query Params)
    - market (market code) : "KRW-BTC"
    - to (last candle, default -> latest)
    - count

Path Params 
    - unit (minute) : 1,3,5,15,10,30,60,240
"""

"""
[
  {
    "market": "KRW-BTC",
    "candle_date_time_utc": "2018-04-18T10:16:00",
    "candle_date_time_kst": "2018-04-18T19:16:00",
    "opening_price": 8615000,
    "high_price": 8618000,
    "low_price": 8611000,
    "trade_price": 8616000, (last_price)
    "timestamp": 1524046594584, (msec)
    "candle_acc_trade_price": 60018891.90054, 
    "candle_acc_trade_volume": 6.96780929,
    "unit": 1
  },
  ...
"""