import websocket
import threading
import orjson
from datetime import datetime
import time

s = websocket.create_connection("ws://0.0.0.0:19999")

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
        s.send(orjson.dumps(data,option= orjson.OPT_NAIVE_UTC))


def handle_command():
    while True:
        data = orjson.loads(s.recv())
        timestamp = data["timestamp"]
        command = data["command"]
        paramter = data["parameter"]

        print(f"Run command : {command}\nParameter:{paramter}")

if __name__ == "__main__":


    data = {
        "type" : "init",
        "timestamp" : datetime.now(),
        "drone_name" : drone_name,
        "drone_info" : drone_info
    }
    s.send(orjson.dumps(data,option= orjson.OPT_NAIVE_UTC))
    
    status_sending_thread = threading.Thread(target=send_status)
    status_sending_thread.start()

    command_thread = threading.Thread(target=handle_command)
    command_thread.start()
