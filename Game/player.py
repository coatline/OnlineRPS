import socket
import player_data


class Player():
    def __init__(self, player_data : player_data.PlayerData, client_number : int, socket : socket.socket) -> None:
        self.player_number = client_number
        self.player_data = player_data
        self.socket = socket