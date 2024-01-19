import jwt  # PyJWT
import uuid, os, sys
import websocket  # websocket-client
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config.config as CONFIG


def on_message(ws, message):
    # do something
    data = message.decode('utf-8')
    print(data)


def on_connect(ws):
    print("connected!")
    # Request after connection
    ws.send('[{"ticket":"test example"},{"type":"myTrade"}]')


def on_error(ws, err):
    print(err)


def on_close(ws, status_code, msg):
    print("closed!")


payload = {
    'access_key': CONFIG.ACCESS_KEY,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, CONFIG.SECRET_KEY)
authorization_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorization_token}

ws_app = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
                                header=headers,
                                on_message=on_message,
                                on_open=on_connect,
                                on_error=on_error,
                                on_close=on_close)


ws_app.run_forever()
