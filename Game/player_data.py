class PlayerData():
    def __init__(self, nickname) -> None:
        # TODO: try to load save from file
        self.wins = 0
        self.games = 0
        self.nickname = nickname
    
    def update_stats(self, won : bool):
        if won:
            self.wins += 1
        
        self.games += 1

        # TODO: save to file