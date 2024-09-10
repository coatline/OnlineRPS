from utilities import *
from player import Player
from game import Game
from user import User

# "_thread" module is lower level than "threading" module
from _thread import *
from data import Data
import socket
import asyncio
import utilities
import pygame
import screen
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
quit_server = False
server = "192.168.1.116"
port = 7777

pygame.init()
screen.initialize()

try:
    server_socket.bind((server, port))
except socket.error as e:
    print(str(e))

# listen for connections 
server_socket.listen()

print("Server started. Waiting for clients to connect.")


games = []
players = []
player_datas = []
# used to remove players when a socket quits
socket_to_player = {}


def create_game(player1 : Player, player2 : Player):
    
    print(f"Creating game: {player1.nickname} vs {player2.nickname}!")

    # create a new game
    new_game = Game(len(games))
    games.append(new_game)
    
    # connect a new player
    new_game.connect_player(player1)
    new_game.connect_player(player2)


async def connect_client(client_socket, addr):
    print(f"Server connected to client address: {addr}")

    # Receive player_data from client
    # task = asyncio.create_task(utilities.receive_data(client_socket, addr))
    data = await utilities.receive_data(client_socket, 1)

    if data == None:
        print("ERROR: I recieved no data.")
        client_socket.close()
        return

    if data.header != "PlayerData":
        print("ERROR: Expected header 'PlayerData' but instead recieved", data.header)

    new_player = Player(data.data, len(players), client_socket)
    players.append(new_player)
    player_datas.append(data.data)

    thread = threading.Thread(target=update_player, args=(new_player,))
    thread.start()


def update_player(player : Player):
    while True:
        if quit_server:
            break
        
        time.sleep(0.5)
        utilities.send_data(player.socket, Data("AllPlayersArray", player_datas))


def accept_connections():
    global quit_server

    while True:
        try:
            # accept any incoming connections and store it's socket and address
            conn, addr = server_socket.accept()
            asyncio.run(connect_client(conn, addr))
        except socket.error as e:
            print(f"Error in server.. {e}")
        
        if quit_server:
            break

thread = threading.Thread(target=accept_connections)
thread.start()


def handle_inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global quit_server

            print("Quitting..")
            quit_server = True

# listen for any incoming connections
while quit_server == False:
    handle_inputs()

server_socket.close()
pygame.quit()
quit()










# from utilities import *
# from player import Player
# from game import Game
# from packet import Packet

# # "_thread" module is lower level than "threading" module
# from _thread import *
# import pickle
# import socket
# import sys

# server = "192.168.1.116"
# port = 7777

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     server_socket.bind((server, port))
# except socket.error as e:
#     print(str(e))

# # listen for 2 connections 
# server_socket.listen(2)

# print("Server started. Waiting for a connection.")

# # start with one game initially
# games = [Game(0)]

# def client_thread(client_socket : socket.socket, game : Game, player : Player):

#     print("Successfully established connection with client.")

#     other_player_index = game.get_other_player_number(player.player_number)

#     # send player object
#     client_socket.send(pickle.dumps(player))

#     # while our client is still connected
#     while True:
#         try:
#             # try to receive 2048 bytes
#             packet = pickle.loads(client_socket.recv(2048))

#             if not packet:
#                 print("Disconnected")
#                 break
#             else:
#                 if packet.header == "Choice":
#                     choice = packet.data

#                     if game.both_went():
#                         winner = game.match_over()

#                 game_socket_pairs[game.id][]

#                 client_socket.send(pickle.dumps())
            
#         except socket.error as e:
#             print(f"Lost connection {e}")
#             break
    
#     print("Closing socket")
#     client_socket.close()


# def connect_client(sock, addr):
#     print(f"Server connecting to client address: {addr}")

#     game_count = len(games)

#     # get latest game
#     game = games[game_count - 1]

#     # if the game is full, create a new one
#     if len(game.players) == 2:
#         game = Game(game_count)
#         games.append(game)
    
#     # connect a new player
#     player_number = len(game.players)
#     new_player = Player(player_number)
#     game.players.append(new_player)
#     game.sockets.append(sock)
    
#     start_new_thread(client_thread, (sock, game, new_player))
#     total_clients += 1

# total_clients = 0

# # listen for any incoming connections
# while True:

#     try:
#         # accept any incoming connections and store it's socket and address
#         conn, addr = server_socket.accept()

#         connect_client(conn, addr)
#     except:
#         server_socket.close()
#         break



# def get_client_index(player_index, game_index):
#     return player_index + (game_index) * 2

# server_socket.close()