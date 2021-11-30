class ActivePlayers:
    _nb_players = 0

    @property
    def nb_players(self):
        return self._nb_players

    @nb_players.setter
    def nb_players(self, increase):
        self._nb_players = increase
        print("Un ajout !", self.nb_players)
