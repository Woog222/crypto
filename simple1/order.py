import pyupbit, json

def make_order(data: dict):
    """
    :param data: received from buy_limit_order OR sell_limit_order
    :return:
    """
    try:
        return Order(
            ticker=data["market"],
            uuid = data["uuid"],
            price = data["price"],
            ord_type = "BID" if data["side"] == "bid" else "ASK",
            volume = data["volume"],
            remaining_volume= data["remaining_volume"]
        )
    except Exception as e:
        print(f"An exception occurred: {type(e).__name__}: {e}")
        print(json.dumps(data, indent=2), flush=True)

class Order:
    def __init__(self, ticker: str, uuid: str, price: float, ord_type: str, volume:float, remaining_volume: float):
        """
        :param ticker:
        :param uuid:
        :param price: order price
        :param ord_type: BID, ASK (limit only)
        :param remaining_volume:
        """
        assert ord_type == "BID" or ord_type == "ASK"
        self.ticker = ticker
        self.uuid = uuid
        self.price = float(price)
        self.ord_type = ord_type
        self.volume = float(volume)

        self.remaining_volume = float(remaining_volume)

    def __str__(self):
        """
        ticker, uuid, ord_type, price, volume, remaining_volume
        """
        return f"{self.ticker}, {self.uuid}, {self.ord_type}, {self.price}, {self.volume}, {self.remaining_volume}"

    def execute(self, executed_volume:float) -> int:
        """

        :param executed_volume:
        :return: 1 (done), 0 (remaining yet)
        """
        assert executed_volume <= self.remaining_volume
        self.remaining_volume -= executed_volume
        return 1 if self.remaining_volume == 0 else 0

    def is_buy(self):
        return self.ord_type == "BID"