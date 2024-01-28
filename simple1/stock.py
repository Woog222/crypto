from abc import *
import pyupbit, sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools.helper import *
import config.config as CONFIG


def calculate_volume(buy_price: float, budget: float):
    """
    for buy_limit_order
    :param buy_price: the target price for order
    :param budget: the amount of money to use
    :return:
    """
    return round(float(budget / buy_price), 8)


class Stock(metaclass=ABCMeta):

    def __init__(self, ticker: str, budget: float, app: pyupbit.Upbit, buy_price: float):
        """
        :param ticker(code):
        :param budget:
        :param app: pyupbit.Upbit object
        """
        self.app = app
        self.ticker = ticker
        self.buy = True
        self.budget = float(budget)
        self.buy_price = float(buy_price)
        self.stop_loss = float(pyupbit.get_tick_size(buy_price * 0.95))
        self.profit_loss = float(pyupbit.get_tick_size(buy_price * 1.01))
        self.shareHeld = 0.0

        chance = app.get_chance(ticker=ticker)
        try:
            self.bid_min_total = float(chance["market"]["bid"]["min_total"])
            self.ask_min_total = float(chance["market"]["ask"]["min_total"])
        except Exception as e:
            print(f"An exception occurred: {type(e).__name__}: {e}")
            print_dict(chance)

    def __str__(self):
        """
        ticker, shareHeld, budget, buy_price, bid_min_total, ask_min_total
        """
        return f"{self.ticker}, {self.shareHeld}, {self.budget}, {self.buy_price}, {self.bid_min_total}, {self.ask_min_total}"

    def buy_and_monitor(self, buy_price:float) -> int:
        """
        :param buy_price:
        :return: 0 (normal), -1 (fail)
        """
        self.buy_price = buy_price = pyupbit.get_tick_size(price=buy_price)
        self.buy_volume = self.volume_caculator(buy_price=buy_price, cur_price=pyupbit.get_current_price(self.ticker))
        res = self.app.buy_limit_order(ticker=self.ticker, price=buy_price, volume=self.buy_volume)

        if "error" in res:
            print(f"error(error[{res['error']['name']}) : {res['error']['message']}")
            return -1
        return 0

    def is_on_buy(self):
        return self.buy

    def buy_done(self):
        self.buy = False

    def add_shareHeld(self, volume:float):
        if self.shareHeld + volume < 0:
            CONFIG.logger.info(f"shareHeld{self.shareHeld}, added volume{volume} ??")
            return
        self.shareHeld += volume

    def liquidate(self):
        # cancel orders
        uuids = [temp["uuid"] for temp in self.app.get_order(self.ticker)]
        for uuid in uuids: self.app.cancel_order(uuid=uuid)
        # liquidation
        remaining_volume = self.app.get_balance(self.ticker)
        self.app.sell_market_order(ticker=self.ticker, volume=remaining_volume)


