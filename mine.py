import pyupbit

if __name__ == "__main__":

    stocks= {"KRW-BTC" : 1, "KRW-ETC":2}

    prices = pyupbit.get_current_price(ticker=list(stocks.keys()))
    print(type(prices))
    print(prices)