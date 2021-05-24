import socket
import time
import json

class Client:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.HEADERSIZE = 10

    def send(self, msg):
        try:
            msg = f"{len(msg):<{self.HEADERSIZE}}"+msg
            self.socket.send(bytes(msg,"utf-8"))
        except ConnectionResetError:
            print(f"[!]Connection closed by server")
            return

    def receive(self, length):
        try:
            msg = self.socket.recv(length)
            return msg
        except ConnectionResetError:
            return "1"

    def wait_for_message(self):
        full_msg = ''
        while True:
            msg = self.receive(16)

            if msg == "1":
                print(f"[!]Connection closed by client {self.address}")
                return msg

            else:
                full_msg += msg[self.HEADERSIZE:].decode("utf-8")
                msglen = int(msg[:self.HEADERSIZE]) - 6

                while msglen > 0:
                    if msglen >= 16:
                        full_msg += self.receive(16).decode("utf-8")
                        msglen -= 16
                    else:
                        full_msg += self.receive(16).decode("utf-8")
                        msglen = 0

                return full_msg
