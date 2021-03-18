import arcade
import os

from view.explosion import Explosion
from view.level import create_wood_block
from view.player import Player
from view.scroll_manage import scroll_manage


class GameView(arcade.View):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        super().__init__()
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.time_taken = 0
        # Sprite lists
        self.wall_list: arcade.SpriteList = None
        self.border_list: arcade.SpriteList = None
        self.player: arcade.SpriteList = None

        # Set up the player
        self.player_sprite: Player = None
        self.physics_engine = None

        self.score = 0
        self.game_over = False

        self.level = 1
        self.max_level = 50

        # scroll (move camera)
        self.view_left = 0
        self.view_bottom = 0

        # Предзагрузка анимации взрыва
        # Pre-load the animation frames. We don't do this in the __init__
        # of the explosion sprite because it takes too long and would cause the game to pause.
        self.explosion_texture_list = []

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"

        # Load the explosions from a sprite sheet
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()

        # Создаём игрока
        self.player_sprite = Player()
        self.player.append(self.player_sprite)

        # Создаём первоночальный блок дерева
        self.border_list, self.wall_list = create_wood_block(self.level)

        # Физический движок для платформера
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.border_list, 0)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Render the screen. Отрисовывает экран
        """
        # Очищаем окно и начинаем отрисовку
        arcade.start_render()

        # Рисуем игрока и брусок
        self.player.draw()
        self.wall_list.draw()
        self.border_list.draw()

        # Рисуем взрыв
        self.explosions_list.draw()

        # Рисуем score на экране
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)

    def on_key_press(self, x=0, y=0, mode="AUTO"):
        """ Called whenever a key is pressed. """
        self.player_sprite.move(x, y, mode)

    def on_key_release(self, key, modifiers=None):
        """ Called when the user releases a key. """
        self.player_sprite.stop(key)

    def on_update(self, delta_time):
        """ Movement and game logic тут происходит действие """
        self.time_taken += delta_time

        # Обновляем игрока используя физический движок
        self.physics_engine.update()

        # Сколько блоков спилили
        block_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.wall_list)
        for wall in block_hit_list:

            # If it did...
            # Make an explosion
            explosion = Explosion(self.explosion_texture_list)
            # Move it to the location of the coin
            explosion.center_x = wall.center_x
            explosion.center_y = wall.center_y
            # Call update() because it sets which image we start on
            explosion.update()
            # Add to a list of sprites that are explosions
            self.explosions_list.append(explosion)

            wall.remove_from_sprite_lists()
            self.score += 1
            self.window.total_score += 1

        self.explosions_list.update()


        # --- Manage Scrolling ---
        # Нужно ли менять view port, если да, то меняем
        self.view_left, self.view_bottom = scroll_manage(self.player_sprite,
                                                         self.view_left, self.view_bottom)


