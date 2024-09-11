from threading import Lock
from server_listener import ServerListener
import json
import socket

class Client:
    def __init__(self, server_host_ip, server_port_tcp = 7777, server_port_udp = 7777, client_port_udp = 7778) -> None:
        self.identifier = None
        self.server_message = []
        self.room_id = None
        self.client_udp_addr = ("0.0.0.0", client_port_udp)
        self.lock = Lock()
        self.server_listener = ServerListener(self.client_udp_addr, self, self.lock)
        self.server_listener.start()
        self.server_udp_addr = (server_host_ip, server_port_udp)
        self.server_tcp_addr = (server_host_ip, server_port_tcp)
        
        self.register()

    def register(self):
        # register client to server and get unique identifier
        print(f"Registering to server at {self.server_tcp_addr}.")

        # send server my port
        message = json.dumps({
            "action": "register",
            "payload": self.client_udp_addr[1]
        })
        
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp_addr)
        self.sock_tcp.send(message.encode())
        data = self.sock_tcp.recv(1024)
        print(f"data recieved: {data}")
        self.sock_tcp.close()
        message = self.parse_data(data)
        self.identifier = message
        print(f"I connected! {self.server_tcp_addr}")
    
    def parse_data(self, data):
        try:
            data = json.loads(data)
            if data['success'] == "True":
                return data['message']
            else:
                raise Exception(data['message'])
        except ValueError:
            print(f"Value Error: {data}")


if __name__ == "__main__":

    is_running = True
    client = Client("192.168.1.116")

    input()
    # while is_running:
    # pass