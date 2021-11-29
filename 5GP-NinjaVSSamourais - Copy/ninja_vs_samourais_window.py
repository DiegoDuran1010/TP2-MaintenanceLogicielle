import arcade

from game import Game
from game import GameState
from game_client import GameClient
from players import Samourai
from players import Player
from tile import Tile
from tile import TileType

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
ORANGE = (255, 192, 0)
SCREEN_TITLE = 'Ninja vs Samouraïs'
REGION_SIZE_X = 50
REGION_SIZE_Y = 50
MOVING_PACE = 5 / 60


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
        arcade.draw_circle_filled(50, 285, 9, arcade.color.RED)
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
        position_de_x = 60
        arcade.draw_text("VIE NINJA", 60, 60, arcade.color.WHITE)

        #boucle qui dessine la barre de vie des ninja
        for i in range(10):
            arcade.draw_circle_filled(position_de_x, 40, 8, arcade.color.RED)
            position_de_x = position_de_x + 20


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
            arcade.draw_text("VIE SAMOURAIS", 300, 60, arcade.color.WHITE)
            position_de_x = 300
            #boucle pour dessiner la barre de vie des samourais
            for j in range(10):
                arcade.draw_circle_filled(position_de_x, 40, 8, arcade.color.GREEN)
                position_de_x = position_de_x + 20


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

            color = Tile.TYPES_AND_COLORS.get(tile.tile_type)
            if not color:
                color = Tile.TYPES_AND_COLORS.get(TileType.GROUND)

            arcade.draw_rectangle_filled(5 + pos[0] * 10,
                                         SCREEN_HEIGHT - (5 + pos[1] * 10), 8, 8, color)

        return ninja_in_viewing_region

    def on_draw(self) -> None:
        """Dessine l'écran sur une base régulière."""
        arcade.start_render()


        arcade.draw_text("VIE SAMOURAIS",300,60,arcade.color.WHITE)
        arcade.draw_circle_filled(300, 40, 8, arcade.color.GREEN)
        arcade.draw_circle_filled(320, 40, 8, arcade.color.GREEN)
        arcade.draw_circle_filled(340, 40, 8, arcade.color.GREEN)
        arcade.draw_circle_filled(360, 40, 8, arcade.color.GREEN)
        arcade.draw_circle_filled(380, 40, 8, arcade.color.GREEN)
        arcade.draw_circle_filled(400, 40, 8, arcade.color.GREEN)
        arcade.draw_circle_filled(420, 40, 8, arcade.color.GREEN)
        arcade.draw_circle_filled(440, 40, 8, arcade.color.GREEN)
        arcade.draw_circle_filled(460, 40, 8, arcade.color.GREEN)
        arcade.draw_circle_filled(480, 40, 8, arcade.color.GREEN)






        if self.__game.state == GameState.PLAYING_LEVEL:
            ninja_in_viewing_region = False

            if self.__game.i_am_the_ninja():
                self.__tiles.draw()  # le ninja voit tout le niveau
            else:
                ninja_in_viewing_region = self.__draw_viewing_region(self.__game)

            if self.__game.i_am_the_ninja() or ninja_in_viewing_region:
                self.__draw_ninja(self.__game)

            self.__draw_samourais(self.__game)




    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.__moving_north = True
        if symbol == arcade.key.DOWN:
            self.__moving_south = True
        if symbol == arcade.key.LEFT:
            self.__moving_west = True
        if symbol == arcade.key.RIGHT:
            self.__moving_east = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.__moving_north = False
        if symbol == arcade.key.DOWN:
            self.__moving_south = False
        if symbol == arcade.key.LEFT:
            self.__moving_west = False
        if symbol == arcade.key.RIGHT:
            self.__moving_east = False

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
