import arcade

from view.constants import MOVEMENT_SPEED


class Player(arcade.Sprite):
    """
    Спрайт пилы
    @x, @y - start position
    """
    def __init__(self, x=50, y=50):
        super().__init__(":resources:images/enemies/saw.png",
                         0.4)
        self.center_x = x
        self.center_y = y
        self.ability_list = arcade.SpriteList()
        self.abilities = arcade.SpriteList()
        self.active_ability_type = 0

    def move(self, x, y):
        self.change_y = y * MOVEMENT_SPEED
        self.change_x = x * MOVEMENT_SPEED

    def stop(self, key):
        self.change_y = 0
        self.change_x = 0



