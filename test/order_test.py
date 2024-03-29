import pyupbit, time, sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config.config as CONFIG
from tools.helper import *
from tools.Monitor import Monitor
from simple1.order import Order

ticker = "KRW-SUI"
cur_price = pyupbit.get_current_price(ticker)
app = pyupbit.Upbit(access=CONFIG.ACCESS_KEY, secret=CONFIG.SECRET_KEY)


if __name__ == '__main__' :
    monitor = Monitor(access_key=CONFIG.ACCESS_KEY, secret_key=CONFIG.SECRET_KEY)
    monitor.start()
    """
        1. buy
    """
    print("1. buy limit : ", end=""); time.sleep(3)
    buy_price = pyupbit.get_tick_size(price=cur_price * 0.7) # 70% price
    temp = app.buy_limit_order(ticker=ticker, price=buy_price, volume=10)
    buy_order = Order(
        ticker=temp["market"],
        uuid = temp["uuid"],
        price = temp["price"],
        ord_type = "BID" if temp["side"] == "bid" else "ASK",
        volume = temp["volume"],
        remaining_volume= temp["remaining_volume"]
    )
    print(buy_order)

    # check it
    buy_limit_uuid = None
    try:
        buy_limit_uuid = temp['uuid']
        temp = app.get_order(ticker_or_uuid=buy_limit_uuid)
        if temp['uuid'] == buy_limit_uuid and temp['state'] == 'wait':
            print("well delivered!")
        else:
            print("not delivered..?")
            print_dict(temp)
    except Exception as e:
        print(f"An exception occurred: {type(e).__name__}: {e}")

    time.sleep(5)
    """
        2. buy cancel
    """
    print("2. buy_cancel : ", end="")
    temp = app.cancel_order(uuid=buy_limit_uuid)

    # check it
    try:
        temp = app.get_order(ticker_or_uuid=buy_limit_uuid)
        if temp['uuid'] == buy_limit_uuid and temp['state'] == 'cancel':
            print("well canceld!")
        else:
            print("not delivered..?")
            print_dict(temp)
    except Exception as x:
        print(x.__class__.__name__)

    """
    3. buy market
    """
    print("3. buy market : ", end="")
    temp = app.buy_market_order(ticker=ticker, price=10000)
    print_dict(temp)
    time.sleep(3)
    # check it
    try:
        buy_market_uuid = temp['uuid']
        temp = app.get_order(ticker_or_uuid=buy_market_uuid)
        if temp['uuid'] == buy_market_uuid and (temp['state'] == 'done' or temp['state'] == 'cancel'):
            print("well executed")
        else:
            print(f"not delivered..? {buy_market_uuid}" )
            print_dict(temp)
    except Exception as x:
        print(x.__class__.__name__)

    # check balance
    temp = app.get_balance(ticker=ticker)
    print(f"{ticker} balance : {temp} now.")

    time.sleep(6)

    """
        4. sell limit
    """
    print("4. sell limit : ", end="")
    cur_price = pyupbit.get_current_price(ticker)
    price = pyupbit.get_tick_size(price=cur_price * 1.3)
    balance = app.get_balance(ticker)

    temp = app.sell_limit_order(ticker=ticker, price=price, volume=balance)

    sell_limit_uuid = None
    # check it
    try:
        sell_limit_uuid = temp['uuid']
        temp = app.get_order(ticker_or_uuid=sell_limit_uuid)
        sell_order = Order(
            ticker=temp["market"],
            uuid=temp["uuid"],
            price=temp["price"],
            ord_type="BID" if temp["side"] == "bid" else "ASK",
            volume=temp["volume"],
            remaining_volume=temp["remaining_volume"]
        )
        if temp['uuid'] == sell_limit_uuid and temp['state'] == 'wait':
            print("well delivered")
        else:
            print("not delivered..?")
            print_dict(temp)
        print(sell_order)
    except Exception as x:
        print(x.__class__.__name__)
    time.sleep(5)

    """
    5. sell cancel
    """

    print("5. sell cancel : ", end="")
    temp = app.cancel_order(uuid=sell_limit_uuid)

    # check it
    temp = app.get_order(ticker_or_uuid=sell_limit_uuid)
    try:
        if temp['uuid'] == sell_limit_uuid and temp['state'] == 'cancel':
            print("well canceld!")
        else:
            print("not delivered..?")
            print_dict(temp)
    except Exception as x:
        print(x.__class__.__name__)

    """
    6. sell market
    """
    print("6. sell market : ", end="")
    temp = app.sell_market_order(ticker=ticker, volume=app.get_balance(ticker=ticker))
    print_dict(temp)
    time.sleep(3)
    # check it
    try:
        sell_market_uuid = temp['uuid']
        temp = app.get_order(ticker_or_uuid=sell_market_uuid)
        if temp['uuid'] == sell_market_uuid and (temp['state'] == 'done' or temp['state'] == 'cancel'):
            print("well executed")
        else:
            print(f"not delivered..? {sell_market_uuid}" )
            print_dict(temp)
    except Exception as x:
        print(x.__class__.__name__)

    # check balance
    temp = app.get_balance(ticker=ticker)
    print(f"{ticker} balance : {temp} now.")
    monitor.terminate()