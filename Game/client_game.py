from button import *
import pickle
import socket
import threading
import client
import screen

def choose_move(move : str):

    print("I chose move:", move)

    for b in buttons:
        b.set_active(False)

    client.client_socket.send(move.encode())


buttons = [Button(50, screen.height / 2, 100, 25, "Rock", (0, 0, 0,), (255, 255, 255), (200, 200, 200), choose_move, "Rock"),
           Button(200, screen.height / 2, 100, 25, "Paper", (0, 0, 0,), (255, 255, 255), (200, 200, 200), choose_move, "Paper"),
           Button(350, screen.height / 2, 100, 25, "Scissors", (0, 0, 0,), (255, 255, 255), (200, 200, 200), choose_move, "Scissors")]

player_number = 0


def check_for_updates():
    global game_data

    while True:
        try:
            new_game_data = client.client_socket.recv(2048)

            if new_game_data != None:
                print("Received new game data!")
                game_data = pickle.loads(new_game_data)
            else:
                print("I received nothing! Time to close the connection and quit!")
                client.client_socket.close()
                quit()
        except socket.error as e:
            print("error!", e)
            client.client_socket.close()


def connection_gained(player_num : int):
    player_number = player_num
    check_thread = threading.Thread(target=check_for_updates)
    check_thread.start()



def update_graphics():
    screen.fill((20, 20, 20))

    for b in buttons:
        b.draw(screen)

    # for thread safety
    current_game_data = game_data
    
    for p in current_game_data.players:
        color = (255, 255, 255)
        text = "Choosing."

        if current_game_data.is_match_over():
            winner = current_game_data.get_winner()

            if p.player_number == winner:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
            
            text = p.choice
        elif p.choice != "":
            text = "Locked in."


        screen.display_text(f"Player {str(p.player_number)}: {text}", color, pygame.Rect((screen.width / 2 - 25), screen.height / 2 + p.player_number * 50, 100, 100), screen.display)

    screen.display_text(f"Wins: " + str(current_game_data.players[player_number].wins), (255, 255, 255), pygame.Rect((screen.width / 2), 25, 100, 100), screen.display)

    # update the display
    pygame.display.flip()

