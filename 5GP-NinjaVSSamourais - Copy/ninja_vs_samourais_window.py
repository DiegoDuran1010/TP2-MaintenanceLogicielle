import arcade

import players
from game import Game
from game import GameState
from game_client import GameClient
from level import PlayersInGame
from players import Samourai
from tile import Tile
from tile import TileType

SCREEN_WIDTH = 575
SCREEN_HEIGHT = 575
BLACK = (0, 0, 0)
ORANGE = (255, 192, 0)
SCREEN_TITLE = 'Ninja vs Samouraïs'
REGION_SIZE_X = 50
REGION_SIZE_Y = 50
MOVING_PACE = 5 / 60


def dont_see_behind_walls(samurai, direction, game):
    wall_position = None
    suite = False
    if direction == "gauche":
        for nb_tiles in range(5):  # moitié de la vue du samourai
            tile = game.level.get_tile(samurai.position[0] - nb_tiles, samurai.position[1])
            if tile.tile_type == TileType.WALL:
                suite = True
            elif tile.tile_type != TileType.WALL and suite:
                tile_position = samurai.position[0] - nb_tiles, samurai.position[1]
                color = (0, 0, 0)
                arcade.draw_rectangle_filled(5 + tile_position[0] * 10,
                                             SCREEN_HEIGHT - (5 + tile_position[1] * 10), 8, 8, color)

    if direction == "droite":
        # Get où est le mur peut importe s'il est dans le viewing_region
        for nb_tiles in range(5):  # moitié de la vue du samourai
            tile = game.level.get_tile(samurai.position[0] + nb_tiles, samurai.position[1])
            if tile.tile_type == TileType.WALL:
                suite = True
            elif tile.tile_type != TileType.WALL and suite:
                tile_position = samurai.position[0] + nb_tiles, samurai.position[1]
                color = (0, 0, 0)
                arcade.draw_rectangle_filled(5 + tile_position[0] * 10,
                                             SCREEN_HEIGHT - (5 + tile_position[1] * 10), 8, 8, color)

    if direction == "haut":
        # Get où est le mur peut importe s'il est dans le viewing_region
        for nb_tiles in range(5):  # moitié de la vue du samourai
            tile = game.level.get_tile(samurai.position[0], samurai.position[1] - nb_tiles)
            if tile.tile_type == TileType.WALL:
                suite = True
            elif tile.tile_type != TileType.WALL and suite:
                tile_position = samurai.position[0], samurai.position[1] - nb_tiles
                color = (0, 0, 0)
                arcade.draw_rectangle_filled(5 + tile_position[0] * 10,
                                             SCREEN_HEIGHT - (5 + tile_position[1] * 10), 8, 8, color)

    if direction == "bas":
        # Get où est le mur peut importe s'il est dans le viewing_region
        for nb_tiles in range(5):  # moitié de la vue du samourai
            tile = game.level.get_tile(samurai.position[0], samurai.position[1] + nb_tiles)
            if tile.tile_type == TileType.WALL:
                suite = True
            elif tile.tile_type != TileType.WALL and suite:
                tile_position = samurai.position[0], samurai.position[1] + nb_tiles
                color = (0, 0, 0)
                arcade.draw_rectangle_filled(5 + tile_position[0] * 10,
                                             SCREEN_HEIGHT - (5 + tile_position[1] * 10), 8, 8, color)

class NinjaVSSamourais(arcade.Window):
    """Fenêtre principale de l'application arcade."""

    def __init__(self, game: Game, game_client: GameClient,
                 width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT, title: str = SCREEN_TITLE):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.__game = game
        self.__game_client = game_client

        self.__tile_shapes = []
        self.__tiles = arcade.ShapeElementList()

        self.__time_since_last_move = 0.0
        self.__moving_east = self.__moving_west = self.__moving_north = self.__moving_south = False

    def attack(self, player_id ):
        tile_position = None
        tiles_list = []
        player = self.__game.get_player(player_id)

        # get le rayon de vue du player jusqu'à un mur ou une roche
        for nb_tiles in range(REGION_SIZE_Y):
            if player.facing_north:
                tile_position = player.position[0], player.position[1] - nb_tiles
            if player.facing_south:
                tile_position = player.position[0], player.position[1] + nb_tiles
            if player.facing_east:
                tile_position = player.position[0] + nb_tiles, player.position[1]
            if player.facing_west:
                tile_position = player.position[0] - nb_tiles, player.position[1]

            tile = self.__game.level.get_tile(tile_position[0], tile_position[1])
            if tile.tile_type == TileType.WALL or tile.tile_type == TileType.STONE:
                break
            else:
                tiles_list.append(tile_position)

        if type(player) == players.Samourai:
            ninja = self.__game.get_player(0)
            if ninja.position in tiles_list:
                ninja.life = player.hit()
                print("je suis le ninja et j'ai une vie de ", ninja.life, "à cause d'une perte de ",
                      player.hit())
            else:
                print("non, je suis a", player.position, " et le samourai est a ", ninja.position)

        if type(player) == players.Ninja:

            for i in range(1, 7):
                samourai = self.__game.get_player(i)
                if samourai.position in tiles_list:
                    samourai.life = player.hit()
                    print("je suis le samourai ", i, " et j'ai une vie de ", samourai.life, "à cause d'une perte de ",
                          player.hit())
                else:
                    print("non, je suis a", player.position, " et le samourai est a ", samourai.position)

    def __build_gui_from_game_level(self) -> None:
        """Construit la grille visuelle représentant le niveau courant."""
        game_level = self.__game.level
        for y in range(game_level.height):
            for x in range(game_level.width):
                tile = game_level.get_tile(x, y)
                tile_color = Tile.TYPES_AND_COLORS
                color = tile_color.get(tile.tile_type)

                if not color:
                    color = tile_color.get(TileType.GROUND)

                shape = arcade.create_rectangle_filled(5 + x * 10, SCREEN_HEIGHT - (5 + y * 10), 8, 8, color)
                self.__tile_shapes.append(shape)
                self.__tiles.append(shape)

    @staticmethod
    def __draw_ninja(game: Game) -> None:
        """Dessine le ninja."""
        ninja = game.get_ninja()
        position = ninja.position[0] * 10
        position1 = ninja.position[1] * 10
        couleur = 6
        couleur2 = 1
        couleur3 = 8

        arcade.draw_rectangle_filled(5 + position, SCREEN_HEIGHT - (5 + position1), couleur3, couleur3,
                                     BLACK)

        if ninja.facing_north:
            pass
        elif ninja.facing_south:
            arcade.draw_rectangle_filled(5 + position, SCREEN_HEIGHT - (3 + position1), couleur3, couleur2,
                                         ORANGE)
        elif ninja.facing_east:
            arcade.draw_rectangle_filled(7 + position, SCREEN_HEIGHT - (3 + position1), couleur, couleur2,
                                         ORANGE)
        else:
            arcade.draw_rectangle_filled(3 + position, SCREEN_HEIGHT - (3 + position1), couleur, couleur2,
                                         ORANGE)

    @staticmethod
    def __draw_samourais(game: Game) -> None:
        """Dessine les samouraïs."""

        for i in range(1, 7):

            samourai = game.get_player(i)

            position = samourai.position[0] * 10
            position2 = (3 + samourai.position[1] * 10)
            position3 = (4 + samourai.position[1] * 10)
            couleur = 2
            couleur2 = 6
            couleur3 = 1
            couleur4 = 8

            arcade.draw_rectangle_filled(5 + position, SCREEN_HEIGHT - (5 + samourai.position[1] * 10),
                                         couleur4, couleur4,
                                         Samourai.COLORS[i - couleur3])
            if samourai.facing_north:
                pass
            elif samourai.facing_south:
                arcade.draw_rectangle_filled(5 + position,
                                             SCREEN_HEIGHT - position2, couleur4, couleur3, BLACK)
                arcade.draw_rectangle_filled(5 + position,
                                             SCREEN_HEIGHT - position3, couleur, couleur, BLACK)
            elif samourai.facing_east:
                arcade.draw_rectangle_filled(7 + position,
                                             SCREEN_HEIGHT - position2, couleur2, couleur3, BLACK)
                arcade.draw_rectangle_filled(8 + position,
                                             SCREEN_HEIGHT - position3, couleur, couleur, BLACK)
            else:
                arcade.draw_rectangle_filled(3 + position,
                                             SCREEN_HEIGHT - position2, couleur2, couleur3, BLACK)
                arcade.draw_rectangle_filled(2 + position,
                                             SCREEN_HEIGHT - position3, couleur, couleur, BLACK)

    @staticmethod
    def __draw_viewing_region(game: Game) -> bool:
        """Dessine le champ de vision du joueur (si samouraï). Retourne True si le ninja s'y trouve."""
        ninja = game.get_ninja()
        ninja_in_viewing_region = False

        # Récupérer le champ de vision du samouraï
        samurai = game.get_current_player()
        viewing_region = samurai.get_viewing_region(50, 50)  # enclin à changer, car champs de vision samurai

        # Afficher les tuiles du champ de vision
        for pos in viewing_region:

            if ninja.position[0] == pos[0] and ninja.position[1] == pos[1]:
                ninja_in_viewing_region = True

            tile = game.level.get_tile(pos[0], pos[1])
            # if tile.tile_type == TileType.WALL:
            if samurai.position[0] < pos[0] and samurai.position[1] == pos[1]:
                # print("mur à droite")
                dont_see_behind_walls(samurai, "droite", game)
            if samurai.position[0] > pos[0] and samurai.position[1] == pos[1]:
                # print("mur à gauche")
                dont_see_behind_walls(samurai, "gauche", game)
            if samurai.position[0] == pos[0] and samurai.position[1] > pos[1]:
                # print("mur en haut")
                dont_see_behind_walls(samurai, "haut", game)
            if samurai.position[0] == pos[0] and samurai.position[1] < pos[1]:
                # print("mur en bas")
                dont_see_behind_walls(samurai, "bas", game)
            # else:
            #     color = Tile.TYPES_AND_COLORS.get(tile.tile_type)
            #     if not color:
            #         color = Tile.TYPES_AND_COLORS.get(TileType.GROUND)

            color = Tile.TYPES_AND_COLORS.get(tile.tile_type)
            if not color:
                color = Tile.TYPES_AND_COLORS.get(TileType.GROUND)

            arcade.draw_rectangle_filled(5 + pos[0] * 10,
                                         SCREEN_HEIGHT - (5 + pos[1] * 10), 8, 8, color)

        return ninja_in_viewing_region

    def on_draw(self) -> None:
        """Dessine l'écran sur une base régulière."""
        arcade.start_render()

        if self.__game.state == GameState.PLAYING_LEVEL:
            ninja_in_viewing_region = False

            if self.__game.i_am_the_ninja():
                self.__tiles.draw()  # le ninja voit tout le niveau
            else:
                ninja_in_viewing_region = self.__draw_viewing_region(self.__game)

            if self.__game.i_am_the_ninja() or ninja_in_viewing_region:
                self.__draw_ninja(self.__game)
            # if PlayersInGame.get_nb_players_in_game() > 1:
            self.__draw_samourais(self.__game)
            # else:
            # print("pas plus d'un joueur ", PlayersInGame.get_nb_players_in_game())
        if self.__game.nb_players() != 0:
            self.draw_linelife()

    def draw_linelife(self):
        """"Affiche les points de vie du ninja et samourais"""
        position_vie_samourai = 60
        position_vie_ninja = 60
        cercle_de_vie = 10

        # boucle qui dessine la barre de vie des ninja et range c par rapport de point vie perso
        if self.__game.i_am_the_ninja(): # self.__game.i_am_the_ninja()
            ninja = self.__game.get_player(0)
            for i in range(ninja.life):
                arcade.draw_text("NINJA", 60, 60, arcade.color.WHITE)
                arcade.draw_circle_filled(position_vie_ninja, 40, cercle_de_vie, arcade.color.RED)
                position_vie_ninja += 20
        else:
            # for i in range(1,7):
            samourai = self.__game.get_player(1)
            vie = samourai.life # ne change pas
            # print("je suis le samourai ", 1, " et ma vie est de ", vie)
            for j in range(vie):
                arcade.draw_text("SAMOURAI", 60, 60, arcade.color.WHITE)
                arcade.draw_circle_filled(position_vie_samourai, 40, cercle_de_vie, arcade.color.GREEN)
                position_vie_samourai += 20

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.__moving_north = True
        if symbol == arcade.key.DOWN:
            self.__moving_south = True
        if symbol == arcade.key.LEFT:
            self.__moving_west = True
        if symbol == arcade.key.RIGHT:
            self.__moving_east = True
        if symbol == arcade.key.LCTRL:
            arcade.close_window()
        if symbol == arcade.key.SPACE:
            self.attack(self.__game.player_id)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.__moving_north = False
        if symbol == arcade.key.DOWN:
            self.__moving_south = False
        if symbol == arcade.key.LEFT:
            self.__moving_west = False
        if symbol == arcade.key.RIGHT:
            self.__moving_east = False
        if symbol == arcade.key.SPACE:
            if self.__game.player_id == 0:
                print("rangement de shuriken")
            else:
                print("rangement du katana par ", self.__game.player_id)


    def on_update(self, delta_time: float):
        self.__game_client.handle_messages(self.__game)

        if self.__game.state == GameState.STARTED:
            self.__game.player_id = self.__game_client.who_am_i()
            self.__game.state = GameState.WAITING_LEVEL
            self.__game_client.send_level_query()
        elif self.__game.state == GameState.LEVEL_RECEIVED:
            self.__build_gui_from_game_level()
            self.__game.state = GameState.PLAYING_LEVEL
        elif self.__game.state == GameState.PLAYING_LEVEL:
            self.__time_since_last_move += delta_time

            if self.__time_since_last_move >= MOVING_PACE:
                self.__time_since_last_move = 0.0
                dispatch_position = False
                player_index = self.__game_client.who_am_i()
                myself = self.__game.get_player(player_index)
                if self.__moving_north:
                    dispatch_position = myself.move_north(self.__game.level)
                if self.__moving_south:
                    dispatch_position = myself.move_south(self.__game.level)
                if self.__moving_west:
                    dispatch_position = myself.move_west(self.__game.level)
                if self.__moving_east:
                    dispatch_position = myself.move_east(self.__game.level)

                if dispatch_position:
                    self.__game_client.send_position(myself.position)
