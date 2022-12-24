import websocket
import threading
import orjson
from datetime import datetime
import time
import rel

with open("config.json", "r") as f:
    data = orjson.loads(f.read())
    drone_name = data["drone_name"]
    drone_info = data["drone_info"]
    drone_status = data["drone_status"]


def send_status():
    global connected
    while connected:
        time.sleep(5)
        data = {
            "type" : "status",
            "timestamp" : datetime.now(),
            "drone_name" : drone_name,
            "drone_status" : drone_status    
        }
        ws.send(orjson.dumps(data,option= orjson.OPT_NAIVE_UTC))

def on_message(ws, message):
    data = orjson.loads(message)
    timestamp = data["timestamp"]
    command = data["command"]
    paramter = data["parameter"]

    print(f"Run command : {command}\nParameter:{paramter}")

def on_error(ws, error):
    print("Error occur :",error)

def on_close(ws, close_status_code, close_msg):
    global connected
    connected = False

def on_open(ws):
    global connected
    connected = True
    data = {
        "type" : "init",
        "timestamp" : datetime.now(),
        "drone_name" : drone_name,
        "drone_info" : drone_info
    }
    ws.send(orjson.dumps(data, option = orjson.OPT_NAIVE_UTC))
    time.sleep(1)
    status_sending_thread.start()


if __name__ == "__main__":
    global connected
    status_sending_thread = threading.Thread(target=send_status)

    connected = True
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://sqcs.tw:8011",
                              on_open = on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close )

    ws.run_forever(dispatcher = rel, reconnect = 5)  
    rel.signal(2, rel.abort)
    rel.dispatch()