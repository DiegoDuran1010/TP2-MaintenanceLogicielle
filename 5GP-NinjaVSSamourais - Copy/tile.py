from enum import Enum
from enum import auto
COULEUR_GROUND = (64, 64, 64)
COULEUR_STONE = (96, 96, 96)


class TileType(Enum):
    GROUND = auto(),
    STONE = auto(),
    WALL = auto(),
    NINJA_START_POS = auto(),
    SAMOURAI_START_POS_1 = auto(),
    SAMOURAI_START_POS_2 = auto(),
    SAMOURAI_START_POS_3 = auto(),
    SAMOURAI_START_POS_4 = auto(),
    SAMOURAI_START_POS_5 = auto(),
    SAMOURAI_START_POS_6 = auto(),
    EXIT = auto()


class Tile:

    TYPES_AND_COLORS = {TileType.GROUND: (64, 64, 64), # !!!
                        TileType.STONE: (96, 96, 96), # !!!
                        TileType.WALL: (255, 255, 255), # !!!
                        TileType.EXIT: (64, 64, 64)} # !!!

    TYPES_AND_SYMBOLS = { ' ': TileType.GROUND,
                         'S': TileType.STONE,
                         'W':TileType.WALL,
                         'N': TileType.NINJA_START_POS,
                         '1':TileType.SAMOURAI_START_POS_1,
                         '2':TileType.SAMOURAI_START_POS_2,
                         '3': TileType.SAMOURAI_START_POS_3,
                         '4':TileType.SAMOURAI_START_POS_4,
                         '5':TileType.SAMOURAI_START_POS_5,
                         '6':TileType.SAMOURAI_START_POS_6,
                         'E':TileType.EXIT}

    #print(TYPES_AND_SYMBOLS)

    #TYPES_AND_SYMBOLS = {v: k for k, v in TYPES_AND_SYMBOLS.items()} # inverser le dict (demander prof que veut dire inverser)
    #print('\n', TYPES_AND_SYMBOLS)

    def __init__(self, walkable: bool = True, tile_type: TileType = TileType.GROUND) -> None:
        self.__walkable = walkable
        self.__tile_type = tile_type

    def __str__(self) -> str:
        return self.TYPES_AND_SYMBOLS[self.__tile_type]

    @staticmethod
    def create_from_symbol(symbol: str):

        """Crée et configure une tuile en fonction du symbole."""
        if symbol == Tile.TYPES_AND_SYMBOLS["S"]:
            return Tile(tile_type=TileType.STONE, walkable=False)
        elif symbol == Tile.TYPES_AND_SYMBOLS["W"]:
            return Tile(tile_type=TileType.WALL, walkable=False)
        elif symbol == Tile.TYPES_AND_SYMBOLS["N"]:
            return Tile(tile_type=TileType.NINJA_START_POS)
        elif symbol == Tile.TYPES_AND_SYMBOLS["1"]:
            return Tile(tile_type=TileType.SAMOURAI_START_POS_1)
        elif symbol == Tile.TYPES_AND_SYMBOLS["2"]:
            return Tile(tile_type=TileType.SAMOURAI_START_POS_2)
        elif symbol == Tile.TYPES_AND_SYMBOLS["3"]:
            return Tile(tile_type=TileType.SAMOURAI_START_POS_3)
        elif symbol == Tile.TYPES_AND_SYMBOLS["4"]:
            return Tile(tile_type=TileType.SAMOURAI_START_POS_4)
        elif symbol == Tile.TYPES_AND_SYMBOLS["5"]:
            return Tile(tile_type=TileType.SAMOURAI_START_POS_5)
        elif symbol == Tile.TYPES_AND_SYMBOLS["6"]:
            return Tile(tile_type=TileType.SAMOURAI_START_POS_6)
        elif symbol == Tile.TYPES_AND_SYMBOLS["E"]:
            return Tile(tile_type=TileType.EXIT)
        else:
            return Tile()

    @staticmethod
    def get_color_for(tile_type: TileType) -> tuple:
        """Retourne la couleur associée au type de tuile spécifié."""

    @property
    def tile_type(self) -> TileType:
        return self.__tile_type

    @property
    def walkable(self) -> bool:
        return self.__walkable
