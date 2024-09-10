from player import Player
import socket

class User:
    def __init__(self, player : Player, socket : socket.socket) -> None:
        self.player = player
        self.socket = socket