import socket, time
import threading

from connection import Connection

def new_connection():
    conn = Connection(socket.gethostname(), 1234)

    conn.send("hello server")
    while True:
        msg = conn.wait_for_message()
        if msg != "1":
            print(f"[>]{msg}")
            time.sleep(1)
            conn.send("hello server")
        else:
            break

new_connection()
