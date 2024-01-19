import asyncio
import json
import jwt
import uuid
import os
import sys
import websocket # websocket-client
import multiprocessing as mp
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools.helper import *

class Monitor(mp.Process):
    def __init__(self, access_key:str, secret_key:str, qsize: int = 1000):
        self.access_key = access_key
        self.secret_key = secret_key
        self.__q = mp.Queue(qsize)
        self.alive = False
        super().__init__()


    def run(self):
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, self.secret_key)
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorization_token}

        self.wsocket = websocket.WebSocketApp(
            "wss://api.upbit.com/websocket/v1",
            header=headers,
            on_message=lambda ws, msg: self.on_message(ws, msg),
            on_ping=lambda: self.on_ping(),
            on_error=lambda ws, msg: self.on_error(ws, msg),
            on_close=lambda ws, status, msg: self.on_close(ws, status, msg),
            on_open=lambda ws: self.on_open(ws)
        )
        self.wsocket.run_forever(ping_interval=10)

    def get(self, timeout:float = -1):
        if not self.alive:
            self.alive = True
            self.start()
        try:
            return self.__q.get(timeout=timeout)
        except Exception as e:
            return {}

    def terminate(self):
        self.alive = False
        super().terminate()

    def on_message(self, ws, message):
        # do something
        data = message.decode('utf-8')
        data = json.loads(data)
        self.__q.put(data)

    def on_ping(self):
        print("ping pong")

    def on_open(self, ws):
        request_str = f'[{{"ticket":"test example"}},{{"type":"myTrade"}}]'
        self.wsocket.send(request_str)
        print("connected. myTrade request is sent to the server.")

    def on_error(self, ws, err):
        print(err)

    def on_close(self, ws, status_code, msg):
        print(f"code({status_code}) : {msg}")




