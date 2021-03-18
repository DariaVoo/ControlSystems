from time import sleep

from parse_json import parse_json


def logic(game_view):
    # game_view.on_key_press(1, 1)
    # sleep(0.1)
    # game_view.on_key_release(0)

    for _ in range(2):
        request = parse_json()
        print(request)
        sleep(0.1)
        if request['mode'] == 'AUTO':
            print('It\'s auto!')
        elif request['mode'] == 'MANUAL':
            print('Manual mode')
            offset_x = int(request['offset']['x'])
            offset_y = int(request['offset']['y'])
            # срезаем юнит = двигаем игрока
            game_view.on_key_press(offset_x, offset_y)
            sleep(0.1)
            game_view.on_key_release(0)


