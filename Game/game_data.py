from player import Player


class GameData:
    def __init__(self) -> None:
        self.players = []
        self.matches_completed = 0


    def update_player(self, player : Player):
        self.players[player.player_number] = player


    def is_match_over(self) -> bool:
        return self.players[0].choice != "" and self.players[1].choice != ""


    def record_match(self) -> Player:
        self.matches_completed += 1
        
        winner_index = self.get_winner()

        winner = None

        # if we didn't tie
        if winner_index != -1:
            winner = self.players[winner_index]
            winner.wins += 1

        return winner


    def get_winner(self) -> int:

        p1 = self.players[0].choice
        p2 = self.players[1].choice

        winner = -1

        if p1 == "Rock" and p2 == "Scissors":
            winner = 0
        elif p1 == "Rock" and p2 == "Paper":
            winner = 1

        elif p1 == "Scissors" and p2 == "Rock":
            winner = 1
        elif p1 == "Scissors" and p2 == "Paper":
            winner = 0
        
        elif p1 == "Paper" and p2 == "Rock":
            winner = 0
        elif p1 == "Paper" and p2 == "Scissors":
            winner = 1

        return winner
    
    def start_new_match(self):
        self.players[0].new_match()
        self.players[1].new_match()