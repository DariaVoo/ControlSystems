from time import sleep

from parse_json import parse_json

def start_cutting(game_view, request):
    '''
    Начинает срезать юниты
    :return: None
    '''
    offset_x = int(request['offset']['x'])
    offset_y = int(request['offset']['y'])
    # срезаем юнит = двигаем игрока
    game_view.on_key_press(offset_x, offset_y)
    sleep(0.1)

def logic(game_view):
    # game_view.on_key_press(1, 1)
    # sleep(0.1)
    # game_view.on_key_release(0)

    for _ in range(2):
        request = parse_json()
        print(request)
        sleep(0.1)
        if request['mode'] == 'MANUAL':
            print('Manual mode')
            start_cutting(game_view, request)
            game_view.on_key_release(0)
        elif request['mode'] == 'AUTO':
            print('It\'s auto!')
            if request['control'] == 'IDLE':
                start_cutting(game_view, request)
            elif request['control'] == 'PAUSE' or request['control'] == 'STOP':
                game_view.on_key_release(0)
                sleep(0.1)
            elif request['control'] == 'CONTINUE':
                start_cutting(game_view, request)






