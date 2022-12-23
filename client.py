import socket
import threading
import time

import orjson
from datetime import datetime

HOST = '0.0.0.0'
PORT = 19999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

drone_name = input("input drone name for test:")
drone_info = {
    "test_info" : "test"
}
drone_status = {
    "test_status" : "rest"
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

if __name__ == "__main__":

    
    s.connect((HOST, PORT))
    data = {
        "type" : "init",
        "timestamp" : datetime.now(),
        "drone_name" : drone_name,
        "drone_info" : drone_info
    }
    tmp = orjson.dumps(data,option= orjson.OPT_NAIVE_UTC)
    print(tmp)
    s.send(tmp)


    status_sending_thread = threading.Thread(target=send_status)
    status_sending_thread.start()


    while True:
        command = s.recv(1024)
        print(command)
        s.send(str(drone_status).encode())


    