import socket
import threading
import sys

from client import Client


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(12)


def new_client(client, address):
    client = Client(client, address)
    while True:
        msg = client.wait_for_message()
        if msg != "1":
            print(f"[>]{msg}")
            client.send("ack")
        else:
            break


while True:
    clientsocket, address = s.accept()
    print(f"[+]Connection from {address} has been established.")

    x = threading.Thread(target=new_client, args=(clientsocket, address,))
    x.start()
