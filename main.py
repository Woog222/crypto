import pyupbit, time
from simple1.trader import Trader
from tools.Monitor import Monitor
import config.config as CONFIG


if __name__ == '__main__':
    app = pyupbit.Upbit(access=CONFIG.ACCESS_KEY, secret= CONFIG.SECRET_KEY)
    monitor = Monitor(access_key=CONFIG.ACCESS_KEY, secret_key=CONFIG.SECRET_KEY)
    monitor.start()
    trader = Trader(app=app, monitor=monitor)

    trader.go()
    trader.add_stock(ticker="KRW-BTC", budget = 6000, buy_price = 57421000)


    while True:
        time.sleep(30)