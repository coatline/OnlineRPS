from player import Player
from game_data import GameData
from user import User

import time
import threading
import pickle
import socket

# communicates between 2 clients, updating their game data's accordingly
class Game:
    def __init__(self, id : int):
        self.players = []
        self.game_data = GameData()
        self.id = id

    def connect_player(self, player : Player):
        
        self.players.append(player)
        self.game_data.players.append(player)

        if self.game_full():
            self.start_game()


    def game_full(self) -> bool:
        return len(self.players) == 2


    def start_game(self):

        # send the users copies of the game data so they know that the game has started
        for i in range(2):
            user : User = self.players[i]

            p_num = user.player.player_number

            user.socket.send(str(p_num).encode())

        time.sleep(1)
        for u in self.players:
            u.socket.send(pickle.dumps(self.game_data))

        # start listening for players' choices
        self.start_new_match()


    def start_new_match(self):
        for user in self.players:
            user_thread = threading.Thread(target=self.listen_for_choices, args=(user,))
            user_thread.start()


    def listen_for_choices(self, user : User):
        
        # while True:
            try:
                # listen for a choice from the user
                choice = user.socket.recv(32).decode()
                
                if choice == None:
                    print(f"Lost connection with player {user.player.player_number}")
                    # user.socket.close()
                    return

                print(f"User {user.player.player_number} chose: {choice}!")

                user.player.choice = choice
                self.update_users_game()
            except socket.error as e:
                print(f"Problem listening for choice on player {user.player.player_number} {e}")


    def update_users_game(self):
        
        for user in self.players:
            self.game_data.update_player(user.player)

        if self.game_data.is_match_over():
            # start a thread that listens for input to ready up for next match.
            # if a new match is agreed on, start a new match

            self.game_data.record_match()
        
        for user in self.players:
            user.socket.send(pickle.dumps(self.game_data))