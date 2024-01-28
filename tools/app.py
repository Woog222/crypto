from abc import *
import pandas as pd


class App(metaclass=ABCMeta):
    """
        order
    """
    @abstractmethod
    def buy_limit_order(self, ticker:str, price: float, volume: float): pass

    @abstractmethod
    def buy_market_order(self, ticker:str, price:float): pass

    @abstractmethod
    def sell_limit_order(self, ticker:str, price:float, volume:float): pass

    @abstractmethod
    def sell_stock_order(self, ticker:str, volume:float): pass









