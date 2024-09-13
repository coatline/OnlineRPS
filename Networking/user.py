import uuid
import json
import socket

class User:
    def __init__(self, addr, udp_port) -> None:
        self.identifier = str(uuid.uuid4())
        self.addr = addr
        self.udp_addr = (addr[0], int(udp_port))

    def send_tcp(self, success, data, sock : socket.socket):
        message = json.dumps({"success": str(success), "message": data})
        sock.send(message.encode())

    def send_udp(self, player_identifier, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps({player_identifier: message}).encode(), self.udp_addr)