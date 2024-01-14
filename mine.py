import pyupbit
import config.config
import time
from tools.helper import *

ticker = "KRW-SUI"
app = pyupbit.Upbit(access=config.config.ACCESS_KEY, secret=config.config.SECRET_KEY)

"""
# 1. buy
print("-------------------- buy limit ---------------------")
cur_price = pyupbit.get_current_price(ticker)
price = pyupbit.get_tick_size(price=cur_price*0.9)
temp = app.buy_limit_order(ticker = ticker, price= price, volume = 10)
print_dict(temp)
uuid = temp['uuid']

time.sleep(5)

# 2. buy cancel
print("--------------------- buy cancel ------------------")
temp = app.cancel_order(uuid=uuid)

print_dict(temp)

print("-------------------- sell limit ---------------------")
cur_price = pyupbit.get_current_price(ticker)
price = pyupbit.get_tick_size(price=cur_price*1.2)

balance = app.get_balance(ticker)

temp = app.sell_limit_order(ticker=ticker, price=price, volume=balance)
print_dict(temp)
uuid = temp['uuid']
time.sleep(5)


print("--------------------- sell cancel ------------------")
temp = app.cancel_order(uuid=uuid)

print_dict(temp)
"""

print("-------------------- buy market ---------------------")


temp = app.buy_market_order(ticker=ticker, price=10000)
print_dict(temp)
uuid = temp['uuid']
time.sleep(5)


print("--------------------- sell market ------------------")
temp = app.sell_market_order(ticker=ticker, volume=app.get_balance(ticker=ticker))

print_dict(temp)