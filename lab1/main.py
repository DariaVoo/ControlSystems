# графика
import arcade

from view.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from view.game import GameView
# логика
from time import sleep
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

GAMEVIEW = None
prev_x = 0
prev_y = 0


def start_cutting(game_view, request):
    """
    Начинает срезать юниты
    :return: None
    """
    global prev_x, prev_y

    offset_x = int(request['offset']['x'])
    offset_y = int(request['offset']['y'])
    print('OFFSETs: ', offset_x, offset_x)
    # учитываем продолжение в режиме CONTINUE с той же скоростью
    if request['mode'] == 'AUTO':
        prev_x = offset_x
        prev_y = offset_y
    # срезаем юнит = двигаем игрока
    sleep(0.1)
    game_view.on_key_press(offset_x, offset_y, request['mode'])
    sleep(0.1)


def logic(request):
    """
    Выполнение команд из json
    :param request: json, полученный с сервера
    :return:
    """
    game_view = GAMEVIEW
    # выполняем запрос
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
            sleep(0.5)
        elif request['control'] == 'CONTINUE':
            sleep(0.1)
            game_view.on_key_press(prev_x, prev_y, request['mode'])
            sleep(0.1)


class S(BaseHTTPRequestHandler):
    """
    Класс обработчик запросов, принимаемых сервером
    """
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        """ получаем json"""
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

        print(str(self.headers))
        content_length = int(self.headers['Dasha-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        print("POST DATA: ", post_data)

        print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
              str(self.path), str(self.headers), post_data.decode('utf-8'))

        # получаем json
        json_data = json.loads(post_data.decode('utf-8'))
        print('My JSON: ', json_data)
        # отрисовываем графику
        logic(json_data)


def run(server_class=HTTPServer, handler_class=S, port=8080):
    """ Запускает сервер """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.total_score = 0

    # создание вьюхи игры
    game_view = GameView()
    game_view.setup()
    window.show_view(game_view)

    global GAMEVIEW
    GAMEVIEW = game_view
    # запуск графики
    game_thread = threading.Thread(target=arcade.run)
    game_thread.start()

    # поднимаем сервер
    run()


if __name__ == "__main__":
    main()
