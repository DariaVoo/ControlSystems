import arcade

SPRITE_SCALING = 0.45
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)


def create_wood_block():
    """
    Создание карты уровня. По факту - наполнение wall_list
    """
    box = ":resources:images/tiles/boxCrate_double.png"
    border = ":resources:images/tiles/brickGrey.png"

    count_row = 150
    count_col = 200

    wall_list = arcade.SpriteList()
    border_list = arcade.SpriteList()

    x = y = 0  # координаты
    for row in range(count_row):  # вся строка
        for col in range(count_col):  # каждый символ
            if col == 0 or col == count_col - 1 \
                    or row == 0 or row == count_row - 1:
                # создаем стену
                wall = arcade.Sprite(border, SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                border_list.append(wall)
            else:
                # создаем блок
                wall = arcade.Sprite(box, SPRITE_SCALING)
                wall.center_x = x
                wall.center_y = y
                wall_list.append(wall)

            x += wall._get_width()  # блоки платформы ставятся на ширине блоков
        y += wall._get_height()  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    # print("WALL",wall._get_width())
    return border_list, wall_list
