import arcade

from constants import MOVEMENT_SPEED, JUMP_SPEED, END_OF_MAP


class Player(arcade.Sprite):
    """
    @x, @y - start position
    """
    def __init__(self, x=50, y=50):
        super().__init__(":resources:images/alien/alienBlue_jump.png",
                         0.3)
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

    def attack(self, enemy_list, score, explosion_texture_list, explosions_list):
        if len(self.ability_list) == 0:
            return 0

        score = 0
        # Loop through each bullet
        for bullet in self.ability_list:
            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.attack(hit_list, explosion_texture_list, explosions_list)
                # Get rid of the bullet
                bullet.remove_from_sprite_lists()

            # For every coin we hit, add to the score and remove the coin
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                score += 5

            # Удаляем вылетившие за уровень пули
            if bullet.center_x > END_OF_MAP:
                bullet.remove_from_sprite_lists()

        return score



