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
        
        self.register_to_server()

    def register_to_server(self):
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

        # recieve connected message that comes with my unique identifier
        
        data = self.sock_tcp.recv(1024)
        

        self.sock_tcp.close()
        message = self.parse_data(data)
        print(f"identifier recieved: {message}")
        self.identifier = message
        print(f"I connected! {self.server_tcp_addr}")
    
    def create_room(self):
        # register client to server and get unique identifier
        print(f"Creating room.")

        message = json.dumps({
            "action": "create_room",
            "identifier": self.identifier,
            "payload": "new room!"
        })
        
        data = self.send_tcp(message)
        
        self.room_id = self.parse_data(data)
        
        print(f"Room successfully created and joined. (room_id: {self.room_id})")

    def get_rooms(self):
        message = json.dumps({
            "action": "leave_room",
            "room_id": self.room_id,
            "identifier": self.identifier
        })
        
        data = self.send_tcp(message)
        
        print(f"Found rooms: ({data})")
        return data

    def leave_room(self):
        message = json.dumps({
            "action": "get_rooms",
            "identifier": self.identifier
        })
        
        self.send_tcp(message)
        print("Left room!")
        

    def send_tcp(self, json):
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp_addr)
        self.sock_tcp.send(json.encode())

        data = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        return self.parse_data(data)

    def parse_data(self, data):
        try:
            data = json.loads(data)
            if data['success'] == "True":
                return data['message']
            else:
                raise Exception(data['message'])
        except ValueError:
            print(f"Value Error: {data}")

    def stop(self):
        if self.room_id != None:
            self.leave_room()
        
        self.server_listener.stop()
        self.server_listener.join()

if __name__ == "__main__":

    is_running = True
    port = input("enter port > ")
    
    client = Client("192.168.1.116", 7777, 7777, int(port))

    while is_running:
        cmd = input()
        if cmd == "quit":
            client.stop()
            quit()
        elif cmd == "create":
            client.create_room()
        elif cmd == "rooms":
            client.get_rooms()
        elif cmd == "leave":
            client.leave_room()