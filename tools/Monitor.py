import asyncio
import json, pyupbit
import uuid
import multiprocessing as mp
import jwt  # PyJWT
import uuid, os, sys
import websocket  # websocket-client
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config.config as CONFIG


class Monitor(mp.Process):
    def __init__(self, access_key:str, secert_key:str, qsize: int = 1000):
        """

        """
        self.access_key = access_key
        self.secret_key = secert_key
        self.__q = mp.Queue(qsize)
        self.alive = False

        super().__init__()

Woog222

    async def __connect_socket(self):
        payload = {
            'access_key': self.access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, self.secret_key)
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorization_token}

        async with websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
                                        header=headers,
                                        on_message=self.on_message,
                                        on_open=self.on_connect,
                                        on_error=self.on_error,
                                        on_close=self.on_close) as wsocket:
            while self.alive:
                    recv_data = await wsocket.recv()
                    recv_data = recv_data.decode('utf8')
                    self.__q.put(json.loads(recv_data))

    def run(self):
        #self.__aloop = asyncio.get_event_loop()
        #self.__aloop.run_until_complete(self.__connect_socket())
        asyncio.run(self.__connect_socket())

    def get(self):
        if self.alive is False:
            self.alive = True
            self.start()
        return self.__q.get()

    def terminate(self):
        self.alive = False
        super().terminate()

    async def on_message(self, wsocket, message):
        data = message.decode('utf-8')
        self.__q.put(data)


    async def on_connect(self, wsocket):
        print(f"websocket connected")


    async def on_error(self, wsocket, error):
        print(f"error : {error}")

    async def on_close(self, wsocket, close_status_code, close_msg):
        print("close connection")

