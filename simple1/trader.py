import sys, os, time, queue
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from simple1.stock import *
from simple1.order import *
from tools.Monitor import Monitor
import threading
import config.config as CONFIG


class Trader(threading.Thread):

    def __init__(self, app: pyupbit.Upbit, monitor: Monitor, sleep_time = 1):
        super().__init__(daemon=True)
        self.app = app
        self.stocks = {} # ticker : Ticker
        self.monitor = monitor
        self.sleep_time = sleep_time
        self.stop_flag = threading.Event()
        self.stock_add_queue = queue.Queue()

        self.running = False
        self.orders = {} # uuid : Order


    def run(self):
        while self.running:
            """
            0. add new stock
            """
            while not self.stop_flag.is_set():
                try:
                    new_stock = self.stock_add_queue.get(block=False)
                except queue.Empty as e:
                    new_stock = None
                if new_stock is None: break

                volume = calculate_volume(buy_price=new_stock.buy_price, budget=new_stock.budget)
                order = make_order(self.app.buy_limit_order(ticker=new_stock.ticker, price=new_stock.buy_price, volume=volume))
                self.stocks[new_stock.ticker] = new_stock
                self.orders[order.uuid] = order

                CONFIG.logger.info(f"{new_stock} added.")
                CONFIG.logger.info(f"new buy order made:")
                CONFIG.logger.info(str(order))

            """
            1. trade info updating
            """
            self.trade_update()
            del_list = []
            for stock in self.stocks.values():
                if not stock.is_on_buy() and self.app.get_balance(stock.ticker )<= 0:
                    del_list.append(stock.ticker)
            for ticker in del_list: self.stocks.pop(ticker)

            """
            2. periodic price check
            """
            if len(self.stocks) > 0:
                prices = pyupbit.get_current_price(ticker=list(self.stocks.keys()))
            else:
                prices = {}

            del_list = []
            for ticker, stock in self.stocks.items():
                if stock.is_on_buy(): continue

                price = prices if isinstance(prices, float) else float(prices[ticker])
                if price < stock.stop_loss:
                    CONFIG.logger.info(f"{ticker} cur({price}) <= {stock.stop_loss}. liquidate it.")
                    stock.liquidate()

            """
            3. get some rest
            """
            time.sleep(self.sleep_time)


    def trade_update(self):
        while True:
            trade_info = self.monitor.get()
            if len(trade_info) == 0: break  # no trade data

            CONFIG.logger.info(f"\nTrade info :")
            CONFIG.logger.info(json.dumps(trade_info, indent=2))

            try:
                uuid = trade_info["order_uuid"]
                ticker = trade_info["code"]

                if uuid not in self.orders:
                    CONFIG.logger.info(f"{uuid} is not in the order list.\n")
                    continue
                if ticker not in self.stocks:
                    CONFIG.logger.info(f"{ticker} is not in the stock list.\n")
                    continue

                order = self.orders[uuid]
                stock = self.stocks[ticker]
                executed_volume = float(trade_info["volume"])

                stock.add_shareHeld(executed_volume if order.is_buy() else ((-1) * executed_volume))
                if order.execute(executed_volume=executed_volume):
                    # order cleared
                    if stock.is_on_buy(): # buy order done
                        new_order = make_order(self.app.sell_limit_order(ticker=ticker, price=stock.profit_loss, volume=stock.shareHeld))
                        self.orders[new_order.uuid] = new_order
                        CONFIG.logger.info(f"new selling order made:")
                        CONFIG.logger.info(str(new_order))
                        stock.buy_done()

                    else: # selling order done
                        stock.liquidate()
                        self.delete_stock(ticker)

            except Exception as e:
                CONFIG.logger.info(f"An exception (trade update) occurred: {type(e).__name__}: {e}")

    def go(self):
        self.running = True
        self.start()

    def quit(self):
        self.running = False
        self.stop_flag.set()

    def add_stock(self, ticker: str, budget: float, buy_price: float):
        new_stock = Stock(ticker=ticker, buy_price=buy_price, budget=budget, app=self.app)
        if budget <= new_stock.bid_min_total + 100:
            CONFIG.logger.info(f"{ticker} : bid min total {new_stock.bid_min_total}. be ready with enough budget.")
            return
        self.stock_add_queue.put(new_stock)




    def delete_stock(self, ticker):
        if ticker not in self.stocks:
            CONFIG.logger.info(f"{ticker} not in stocks. (current : {self.stocks.keys()})")
            return

        stock = self.stocks[ticker]
        if stock.shareHeld > 0:
            CONFIG.logger.info(f"{ticker} shareHeld({stock.shareHeld}), but deleted.")
        if CONFIG.DEBUG:
            CONFIG.logger.info(f"{self.stocks[ticker]} deleted.")
        self.stocks.pop(ticker)