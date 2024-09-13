from threading import Thread, Lock
import socket

class ServerListener(Thread):
    def __init__(self, udp_addr, client, lock : Lock):
        Thread.__init__(self)

        self.client = client
        self.lock = lock
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.bind(udp_addr)
        
        # self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.tcp_sock.bind(tcp_addr)

    def run(self):
        while True:
            # receieve udp packets
            data, addr = self.udp_sock.recvfrom(1024)
            self.lock.acquire()
            try:
                print(f"recieved UDP data: {data}")
                self.client.server_message.append(data)
            finally:
                self.lock.release()

    # on thread stop
    def stop(self):
        self.udp_sock.close()