import websocket
import threading
import orjson
from datetime import datetime
import time
import rel


drone_name = input("input drone name:")
drone_info = {
    "test_info" : "test"
}
drone_status = {
    "test_status" : "test"
}

def send_status():
    while True:
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
    pass

def on_open(ws):
    pass


if __name__ == "__main__":

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://sqcs.tw:8011",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)  
    rel.signal(2, rel.abort) 
    rel.dispatch()

    data = {
        "type" : "init",
        "timestamp" : datetime.now(),
        "drone_name" : drone_name,
        "drone_info" : drone_info
    }
    ws.send(orjson.dumps(data,option= orjson.OPT_NAIVE_UTC))
    
    status_sending_thread = threading.Thread(target=send_status)
    status_sending_thread.start()