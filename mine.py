import jwt  # PyJWT
import uuid, os, sys
import websocket  # websocket-client
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools.Monitor import Monitor
import config.config as CONFIG
from tools.helper import *


if __name__ == "__main__":
    monitor = Monitor(access_key=CONFIG.ACCESS_KEY, secret_key=CONFIG.SECRET_KEY)

    while True:
        print("hi")
        data = monitor.get(timeout=3)
        if len(data) == 0: # empty dict, no trade data
            print("no trade")
            continue
        print_dict(data)

