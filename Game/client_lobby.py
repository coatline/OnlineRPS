from game_data import GameData
import screen
import pygame
import client
import pickle
import button

buttons = []

def start_game():
    game_data : GameData = pickle.loads(client.client_socket.recv(2048))

    # print(f"Game started. I'm player {player_number}")
    # pygame.display.set_caption(f"Client {player_number}")

def display(other_players : list):

    screen.display.fill((10, 10, 10))

    buttons = []

    num = 0

    for player in other_players:
        buttons.append(button.Button(screen.width / 2, screen.height / 2 + 35 * num, 130, 30, player.nickname, (0, 0, 0,), (255, 255, 255), (200, 200, 200), start_game))
        num += 1

    if len(buttons) == 0:
        screen.display_text("Waiting for other players.", (255, 255, 255), pygame.Rect(screen.width / 2, screen.height / 5, 100, 50), screen.display)
    
    for b in buttons:
        b.draw(screen.display)

    pygame.display.flip()



def handle_input():
    for event in pygame.event.get():
        for b in buttons:
            b.handle_event(event)

def update(other_players : list):
    display(other_players)
    handle_input()

    
# class Scene:
#     def __init__(self, name : str) -> None:
#         buttons = []
#         pass

#     def handle_input(event : pygame.event):
#         pass

#     def display():
#         pass