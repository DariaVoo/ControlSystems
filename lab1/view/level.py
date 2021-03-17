import arcade

SPRITE_SCALING = 0.45
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

lvl1 = [
    "*************************",
    "*                       *",
    "*   -----------         *",
    "*   -----------         *",  # и тут лагает
    "*   -----------         *",  # здесь лагает почему-то
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*   -----------         *",
    "*                       *",
    "*************************"]


def create_wood_block(lvl=1):
    """
    Создание карты уровня. По факту - наполнение wall_list
    """
    box = ":resources:images/tiles/boxCrate_double.png"
    border = ":resources:images/tiles/brickGrey.png"

    level = lvl1

    wall_list = arcade.SpriteList()
    border_list = arcade.SpriteList()
    # ДОЛЖНО ГЕНЕРИРОВАТЬСЯ
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                # создаем блок
                wall = arcade.Sprite(box, SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                wall_list.append(wall)
            elif col == "*":
                # создаем стену
                wall = arcade.Sprite(border, SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                border_list.append(wall)

            x += wall._get_width()  # блоки платформы ставятся на ширине блоков
        y += wall._get_height()  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    return border_list, wall_list
