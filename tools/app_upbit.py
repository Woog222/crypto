import sys, os, jwt, hashlib, requests, uuid, math
from urllib.parse import urlencode, unquote
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
        self.access_key = access_key
        self.secret_key = secret_key
        # check validity

        self.ticker_info = {}
        """
        self.ticker_info[ticker] = {
            "bid_fee": float(res['bid_fee']),
            "ask_fee": float(res['ask_fee']),
            "bid_types": res['market']['bid_types'],
            "ask_types": res['market']['ask_types'],
            "bid_min_total": float(res['market']['bid']['min_total']),
            "ask_min_total": float(res['market']['ask']['min_total']),
            "max_total": float(res['market']['max_total']),
        }
        """

    def _request_headers(self, query=None):
        payload = {
            "access_key": self.access_key,
            "nonce": str(uuid.uuid4())
        }

        if query is not None:
            m = hashlib.sha512()
            m.update(urlencode(query, doseq=True).replace("%5B%5D=", "[]=").encode())
            query_hash = m.hexdigest()
            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = "SHA512"

        jwt_token = jwt.encode(payload, self.secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorization}
        return headers

    def buy_limit_order(self, ticker: str, price: float, volume: float):
        """
        Limit order (KRW only)
        :param ticker:
        :param price:
        :param volume: d
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        #if ticker not in self.ticker_info: self.subscribe(ticker)
        # send order
        try:
            url = CONFIG.SERVER_URL + "/v1/orders"
            params = {"market": ticker,
                    "side": "bid",
                    "volume": str(volume),
                    "price": str(price),
                    "ord_type": "limit"}
            headers = self._request_headers(params)
            res = requests.post(url, json=params, headers=headers)
            return res.json()
        except Exception as x:
            print(x.__class__.__name__)
            return None


    def buy_market_order(self, ticker: str, price: float):
        pass

    def subscribe(self, ticker) -> None:
        """
        :param ticker
        :param
        :return:
        """
        if ticker in self.ticker_info: return
        try:
            url = CONFIG.SERVER_URL + "/v1/orders/chance"
            params = {"market": ticker}
            headers = self._request_headers(params)
            res = requests.get(url, headers=headers, params=params).json()
            self.ticker_info[ticker] = {
                "bid_fee": float(res['bid_fee']),
                "ask_fee": float(res['ask_fee']),
                "bid_types": res['market']['bid_types'],
                "ask_types": res['market']['ask_types'],
                "bid_min_total": float(res['market']['bid']['min_total']),
                "ask_min_total": float(res['market']['ask']['min_total']),
                "max_total": float(res['market']['max_total']),
            }

        except Exception as x:
            print(x.__class__.__name__)
            return

    def unsubscribe(self, ticker:str) -> None:
        if ticker in self.ticker_info:
            self.ticker_info.pop(ticker)


