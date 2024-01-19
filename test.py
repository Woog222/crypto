"""
import os
import subprocess

test_path = 'test'

# Iterate over all files in the directory
for filename in os.listdir(test_path):
    if filename.endswith('.py'):
        script_path = os.path.join(test_path, filename)

        print(f"--------- {script_path} -----------")
        result = subprocess.run(['python', script_path])
        if result.returncode != 0:
            print(f"return code : {result.returncode}", end="\n\n")
"""
import jwt  # PyJWT
import uuid
import websocket  # websocket-client

import config.config


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
    'access_key': config.config.ACCESS_KEY,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, config.config.SECRET_KEY);
authorization_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorization_token}

ws_app = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
                                header=headers,
                                on_message=on_message,
                                on_open=on_connect,
                                on_error=on_error,
                                on_close=on_close)
ws_app.run_forever()

