from threading import Thread, Lock
import socket

class ServerListener(Thread):
    def __init__(self, addr, client, lock : Lock):
        Thread.__init__(self)

        self.client = client
        self.lock = lock
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(addr)

    def run(self):
        while True:
            # receieve udp packets
            data, addr = self.sock.recvfrom(1024)
            self.lock.acquire()
            try:
                self.client.server_message.append(data)
            finally:
                self.lock.release()

    # on thread stop
    def stop(self):
        self.sock.close()