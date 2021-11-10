from enum import Enum
from enum import auto


from level import Level
from players import Ninja
from players import Samourai


class GameState(Enum):
    STARTING = auto(),
    STARTED = auto(),
    WAITING_LEVEL = auto(),
    LEVEL_RECEIVED = auto(),
    PLAYING_LEVEL = auto()


class Game:
    """Données relatives à la partie en cours."""
    def __init__(self) -> None:
        self.__level_number = 0
        self.__level = None

        self.player_id = -1
        self.__player_is_ninja = False
        self.__players = []

        self.state = GameState.STARTING

    def __create_ninja_and_samourais(self):
        """Instancie le ninja et les samouraïs."""
        player_positions = self.level.get_starting_positions()
        self.__players.append(Ninja(player_positions[0]['x'], player_positions[0]['y']))
        for i in range(6):
            self.__players.append(Samourai(player_positions[i+1]['x'], player_positions[i+1]['y']))

    #Verifier si le joueur est le ninja
    def i_am_the_ninja(self) -> bool:
        return self.__player_is_ninja

    #Declare le ninja
    def declare_ninja(self) -> None:
        self.__player_is_ninja = True

    #c'est qui les utilisateur
    def get_current_player(self):
        return self.__players[self.player_id]

    def get_ninja(self) -> Ninja:
        return self.__players[0]

    # c'est combien les utilisateur
    def get_player(self, player_id: int):
        return self.__players[player_id]

    #Change le prochain niveau et créer le ninja et samurais
    def next_level(self) -> None:
        self.__level_number += 1
        self.__level = Level()
        self.level.load(self.__level_number)
        self.__create_ninja_and_samourais()

    #Set le niveau
    def set_level(self, level) -> None:
        self.__level = level
        self.__create_ninja_and_samourais()

    #update la position du joueur, selon le ID du joueur
    def update_player_position(self, player_id: int, position: tuple) -> None:
        player = self.__players[player_id]
        player.position = position

    #Getter du level
    @property
    def level(self) -> Level or None:
        return self.__level

    #Getter du ID player
    @property
    def player_id(self) -> int:
        return self.__player_id

    #Getter du state
    @property
    def state(self) -> GameState:
        return self.__state

    #Setter du id joueur
    @player_id.setter
    def player_id(self, player_id) -> None:
        self.__player_id = player_id

    #Setter du state
    @state.setter
    def state(self, state) -> None:
        self.__state = state
