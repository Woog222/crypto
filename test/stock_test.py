import pyupbit, time, sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config.config as CONFIG
from simple1.stock import Stock
from tools.helper import *


if __name__ == "__main__":
    app = pyupbit.Upbit(access=CONFIG.ACCESS_KEY, secret=CONFIG.SECRET_KEY)
    stock = Stock("KRW-BTC", alloc_money=100000, app=app)
    print(stock)