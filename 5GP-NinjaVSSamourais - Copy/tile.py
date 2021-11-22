from enum import Enum
from enum import auto

COULEUR_GROUND = (64, 64, 64)
COULEUR_STONE = (96, 96, 96)
COULEUR_WALL = (255, 255, 255)


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
    EXIT = auto(),
    WALKABLE = False


class Tile:
    TYPES_AND_COLORS = {TileType.GROUND: COULEUR_GROUND,
                        TileType.STONE: COULEUR_STONE,
                        TileType.WALL: COULEUR_WALL,
                        TileType.EXIT: COULEUR_GROUND}

    TYPES_AND_SYMBOLS = {' ': TileType.GROUND,
                         'S': TileType.STONE,
                         'W': TileType.WALL,
                         'N': TileType.NINJA_START_POS,
                         '1': TileType.SAMOURAI_START_POS_1,
                         '2': TileType.SAMOURAI_START_POS_2,
                         '3': TileType.SAMOURAI_START_POS_3,
                         '4': TileType.SAMOURAI_START_POS_4,
                         '5': TileType.SAMOURAI_START_POS_5,
                         '6': TileType.SAMOURAI_START_POS_6,
                         'E': TileType.EXIT,
                         TileType.WALKABLE : False}

    def __init__(self, walkable: bool = True, tile_type: TileType = TileType.GROUND) -> None:
        self.__walkable = walkable
        self.__tile_type = tile_type

    def __str__(self) -> str:
        for value in self.TYPES_AND_SYMBOLS:
            if self.TYPES_AND_SYMBOLS[value] == self.__tile_type:
                return value

    @staticmethod
    def create_from_symbol(symbol: str):

        """Crée et configure une tuile en fonction du symbole."""
        if symbol == "S":
            return Tile(tile_type=TileType.STONE, walkable=Tile.TYPES_AND_SYMBOLS[TileType.WALKABLE])
        elif symbol == "W":
            return Tile(tile_type=TileType.WALL, walkable=Tile.TYPES_AND_SYMBOLS[TileType.WALKABLE])
        elif symbol == "N":
            return Tile(tile_type=TileType.NINJA_START_POS)
        elif symbol == "1":
            return Tile(tile_type=TileType.SAMOURAI_START_POS_1)
        elif symbol == "2":
            return Tile(tile_type=TileType.SAMOURAI_START_POS_2)
        elif symbol == "3":
            return Tile(tile_type=TileType.SAMOURAI_START_POS_3)
        elif symbol == "4":
            return Tile(tile_type=TileType.SAMOURAI_START_POS_4)
        elif symbol == "5":
            return Tile(tile_type=TileType.SAMOURAI_START_POS_5)
        elif symbol == "6":
            return Tile(tile_type=TileType.SAMOURAI_START_POS_6)
        elif symbol == "E":
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
