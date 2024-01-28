import sys, os, jwt, hashlib, requests, uuid, math
from urllib.parse import urlencode, unquote
import pyupbit

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config.config as CONFIG
from tools.app import App

def get_tick_size(price, method="floor"):
    """원화마켓 주문 가격 단위

    Args:
        price (float]): 주문 가격
        method (str, optional): 주문 가격 계산 방식. Defaults to "floor".

    Returns:
        float: 업비트 원화 마켓 주문 가격 단위로 조정된 가격
    """

    if method == "floor":
        func = math.floor
    elif method == "round":
        func = round
    else:
        func = math.ceil

    if price >= 2000000:
        tick_size = func(price / 1000) * 1000
    elif price >= 1000000:
        tick_size = func(price / 500) * 500
    elif price >= 500000:
        tick_size = func(price / 100) * 100
    elif price >= 100000:
        tick_size = func(price / 50) * 50
    elif price >= 10000:
        tick_size = func(price / 10) * 10
    elif price >= 1000:
        tick_size = func(price / 5) * 5
    elif price >= 100:
        tick_size = func(price / 1) * 1
    elif price >= 10:
        tick_size = func(price / 0.1) / 10
    elif price >= 1:
        tick_size = func(price / 0.01) / 100
    elif price >= 0.1:
        tick_size = func(price / 0.001) / 1000
    else:
        tick_size = func(price / 0.0001) / 10000

    return tick_size

class AppUpbit(App):

    def __init__(self, access_key:str, secret_key:str) -> None:
        self.upbit = pyupbit.Upbit(access=access_key, secret=secret_key)

    def buy_limit_order(self, ticker: str, price: float, volume: float):
        self.upbit.buy_limit_order(ticker=ticker, price=price, volume=volume)

    def buy_market_order(self, ticker: str, price: float):
        self.upbit.buy_market_order(ticker=ticker, price=price)

    def sell_limit_order(self, ticker: str, price: float, volume: float):
        self.upbit.sell_limit_order(ticker=ticker, price=price, volume=volume)

    def sell_stock_order(self, ticker: str, volume: float):
        self.upbit.sell_market_order(ticker=ticker, volume=volume)





