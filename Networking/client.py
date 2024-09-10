from player import Player
from game_data import GameData
from button import *

from player_data import PlayerData
from player import Player
import utilities
import data
import time
import asyncio
import screen
import pygame
import socket
import pickle
import client_game
import client_lobby

screen.initialize()

# SETUP CONNECTION TO SERVER
client_socket : socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "192.168.1.116"
port = 7777

persist_server_thread : threading.Thread = None
connected_to_server : bool = False
quit_game : bool = False
other_players = []
nickname = "Johnny123"

def update_graphics():
    screen.display.fill((50, 10, 10))
    screen.display_text("Connecting to server...", (255,255,255), pygame.Rect((screen.width / 2 - 25), screen.height / 2, 100, 100), screen.display)
    pygame.display.flip()

def update():
    run = True
    clock = pygame.time.Clock()

    while run:
       
        handle_inputs()
        
        if connected_to_server == False:
            update_graphics()
        else:
            client_lobby.update(other_players=other_players)

        # limit framerate
        clock.tick(60)


def handle_inputs() -> bool:
    global quit_game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            print("Quitting..")

            # if utilities.is_connection_alive(client_socket):
            #     client_socket.close()
            
            quit_game = True
            pygame.quit()
            quit()

    return True


async def connect_to_lobby():
    global other_players
    
    data = await utilities.receive_data(client_socket)

    if data == None:
        return

    if data.header == "AllPlayersArray":
        other_players = list(data.data)

    for player in other_players:
        print(player.nickname)



async def try_connect_to_server():
    global client_socket
    global connected_to_server

    print("Attempting to connect")
    await utilities.setup_connection(server, port, client_socket)
    print("Connected. Sending PlayerData now.")
    
    utilities.send_data(client_socket, data.Data("PlayerData", PlayerData(nickname)))
    connected_to_server = True
    
    while True:
        if quit_game:
            break

        await connect_to_lobby()
        asyncio.sleep(1)

def persist_server_connection():
    global connected_to_server

    while True:
        if connected_to_server:
            # # Check for server disconnect
            # if utilities.is_connection_alive(client_socket) == False :
            #     connected_to_server = False
            #     print("Server Close Detected!")
            # else:
            #     print("just checking..")

            # readable, _, _ = select.select([client_socket], [], [], 0)
            # if not readable:
            #     print("Socket is not readable, may be closed")
            #     connected_to_server = False


            time.sleep(1)
        else:
            asyncio.run(try_connect_to_server())

        if quit_game:
            break


if __name__=="__main__":
    persist_server_thread = threading.Thread(target=persist_server_connection)
    persist_server_thread.start()

    update()