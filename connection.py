import socket

class Connection:
    def __init__(self, address, port):
        self.HEADERSIZE = 10
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((address, port))

    def send(self, msg):
        try:
            msg = f"{len(msg):<{self.HEADERSIZE}}"+msg
            self.connection.send(bytes(msg,"utf-8"))
        except ConnectionResetError:
            print(f"[!]Connection closed by server")
            return

    def receive(self, length):
        try:
            msg = self.connection.recv(length)
            return msg
        except ConnectionResetError:
            return "1"

    def wait_for_message(self):
        full_msg = ''
        while True:
            msg = self.receive(16)

            if msg == "1":
                print(f"[!]Connection closed by server")
                return "1"

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
