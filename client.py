from threading import Lock
from server_listener import ServerListener
import json
import socket

class Client:
    def __init__(self, server_host_ip, server_port_tcp = 7777, server_port_udp = 7778, client_port_udp = 7779) -> None:
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
        print(f"> Registering to server at {self.server_tcp_addr}.")

        # send server my port
        to_send = json.dumps({
            "action": "register",
            "payload": self.client_udp_addr[1]
        })
        
        data = self.send_tcp(to_send)
        self.identifier = data
        print(f"> identifier recieved: {data}. Connected to {self.server_tcp_addr}.")
    
    def create_room(self, room_name):
        if self.room_id != None:
            print("> Already in a room!")
            return

        to_send = json.dumps({
            "action": "create_room",
            "identifier": self.identifier,
            "payload": room_name
        })
        
        data = self.send_tcp(to_send)
        self.room_id = data
        
        print(f"> Room '{room_name}' successfully created and joined.")

    def get_rooms(self):
        to_send = json.dumps({
            "action": "get_rooms",
            "room_id": self.room_id,
            "identifier": self.identifier
        })
        
        data = self.send_tcp(to_send)
        
        print(f"> Found rooms: ({data})")
        return data

    def join_room(self, room_name):
        to_send = json.dumps({
            "action": "join_room",
            "payload": room_name,
            "identifier": self.identifier
        })
        
        try:
            data = self.send_tcp(to_send)
            self.room_id = data
            print(f"> Room joined. (room_id: {self.room_id})")
        except Exception as e:
            print(f"> Error joining that room! {e}")

    def auto_join(self):
        to_send = json.dumps({
            "action": "auto_join",
            "identifier": self.identifier
        })
        
        data = self.send_tcp(to_send)
        self.room_id = data
        print(f"> Joined an open room ({self.room_id})")

    def try_leave_room(self):
        if self.room_id == None:
            print("> I'm not in a room!")
            return
        
        to_send = json.dumps({
            "action": "leave_room",
            "room_id" : self.room_id,
            "identifier": self.identifier
        })
        
        self.send_tcp(to_send)
        self.room_id = None
        print("> Left room!")
        
    def send_to_all(self, message):
        if self.room_id == None:
            print("> Join a room first!")
            return
        
        to_send = json.dumps({
            "action": "send_to_all",
            "payload": {"message": message},
            "room_id": self.room_id,
            "identifier": self.identifier
        })
        
        print(f"> Sending {message} to all.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(to_send.encode(), self.server_udp_addr)

    # Not tested probably doesn't work
    def send_to(self, recipients, message):
        if self.room_id == None:
            print("> Join a room first!")
            return
        
        to_send = json.dumps({
            "action": "send_to",
            "payload": {
                "recipients": recipients,
                "message": message
            },
            "room_id": self.room_id,
            "identifier": self.identifier
        })
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(to_send.encode(), self.server_udp_addr)
        
    def send_tcp(self, to_send):
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp_addr)
        self.sock_tcp.send(to_send.encode())

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
            print(f"> Value Error: {data}")

    def stop(self):
        self.try_leave_room()
        self.server_listener.stop()
        self.server_listener.join()

if __name__ == "__main__":

    is_running = True
    my_port = input("> enter port: ")
    
    client = Client("192.168.1.116", 7777, 7778, int(my_port))

    while is_running:
        
        cmd = input()
        
        words = cmd.split()
        first_word = words[0]
                
        rest = cmd[len(first_word):]
        
        if rest != None and rest != "":
            rest = rest[1:]
        
        if cmd == "quit":
            client.stop()
            quit()
        elif first_word == "create":
            client.create_room(rest)
        elif cmd == "rooms":
            client.get_rooms()
        elif cmd == "leave":
            client.try_leave_room()
        elif first_word == "send":
            client.send_to_all(rest)
        elif first_word == "join":
            client.join_room(rest)
        elif first_word == "autojoin":
            client.auto_join()