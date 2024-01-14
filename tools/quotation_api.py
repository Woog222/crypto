import sys, os, json, requests
import pandas as pd
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config.URL as URL


def get_minute_charts(code:str, count:int, unit:int) -> pd.DataFrame:
    """
    :param code:
    :param count:
    :param unit:
        [
            {
                'code' : data['market'],
                'opening_price' : int(data['opening_price']),
                'trade_price' : int(data['trade_price']),
                'high_price' : int(data['high_price']),
                'low_price' : int(data['low_price']),
                'time_stamp' : int(data['timestamp']) / 1000,
                'acc_trade_price' : float(data['candle_acc_trade_price']),
                'acc_trace_volume' : float(data['candle_acc_trade_volume']),
                'real_time' : datetime.fromtimestamp(int(data['timestamp']) / 1000)
            }, ..
        ]
    :return:
        - pd.DataFrame (success)
        - None (fail)
    """
    url = URL.MINUTE_CANDLE + f"/{unit}"+ f"?market={code}" + f"&count={count}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # list with dict elements
        response_dict = json.loads(response.text)

        ret = None
        for data in response_dict:

            candle = {
                #'code' : data['market'],
                'opening_price' : float(data['opening_price']),
                'trade_price' : float(data['trade_price']),
                'high_price' : float(data['high_price']),
                'low_price' : float(data['low_price']),
                'time_stamp' : int(data['timestamp']) / 1000,
                'acc_trade_price' : float(data['candle_acc_trade_price']),
                #'acc_trace_volume' : float(data['candle_acc_trade_volume']),
                #'real_time' : datetime.fromtimestamp(int(data['timestamp']) / 1000)
            }

            if ret is None: # first row
                ret = pd.DataFrame(candle, index=[0])
            else: # add
                new_df = pd.DataFrame(candle, index=[0])
                ret = pd.concat([ret, new_df], ignore_index=True)
        ret.reset_index(inplace=True, drop=True)
        return ret

    else:
        print(f"Request failed with status code {response.status_code}", file=sys.stderr)
        print(response.text, file=sys.stderr)
        return None

def get_tickers(exclude_warning:bool = False, KRW:bool = True) -> list:
    """
    :return:
        - code list (success)
        - empty list (fail)
    """
    url = URL.MARKET_CODE + f"?isDetails={'true' if exclude_warning else 'false'}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # list with dict elements
        response_dict = json.loads(response.text)
        codes = []
        for market_data in response_dict:
            if exclude_warning and market_data['market_warning'] == 'CAUTION': continue
            if KRW and market_data["market"].split("-")[0] != "KRW": continue
            if not KRW and market_data["market"].split("-")[0] == "KRW":  continue
            codes.append(market_data['market'])
        return codes
    else:
        print(f"Request failed with status code {response.status_code}", file=sys.stderr)
        print(response.text, file=sys.stderr)
        return []