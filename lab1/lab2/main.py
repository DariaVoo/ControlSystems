from io import BytesIO

import numpy as np
# логика
from time import sleep
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from lab2.funs import inertia_free, clean_lag, aperiodic_link, black_box


def logic(request):
    """
    Выполнение команд из json
    :param request: json, полученный с сервера
    :return:
    """
    config = request["config"]
    type_obj = config["objectType"]
    hyper_param = config["hyperParam"]
    is_h = config["isWeightAccepted"]
    x = request["inputSignal"]["values"]

    y = None
    if type_obj == 'BIINERTIAL':
        print('Безинерционный объект')
        x = np.asarray(x)
        y = inertia_free(x, use_h=is_h, k=hyper_param)
    elif type_obj == 'NET_LAG':
        print('Чистое запаздывание')
        y = clean_lag(x, use_h=is_h, i_lag=hyper_param)
    elif type_obj == 'APERIODIC_LINK':
        print('Апериодический сигнал')
        y = aperiodic_link(x, use_h=is_h, period=hyper_param)
    elif type_obj == 'BLACK_BOX':
        print('Чёрный ящик')
        y = black_box(x, use_h=is_h, L=hyper_param)
    print('Вычисления готовы')
    return y


class S(BaseHTTPRequestHandler):
    """
    Класс обработчик запросов, принимаемых сервером
    """
    def _set_response(self, y=0):
        str_send = ''

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        for s in y:
            str_send += str(s)
            str_send += ','
        print('will sent', str_send)

        self.wfile.write(str_send.encode())
        print('sent responce!')

    def do_GET(self):
        print("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))


    def do_POST(self):
        """ получаем json"""
        # self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        if self.path == "/dasha":
            print(str(self.headers))
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            print(content_length)
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself
            print("POST DATA: ", post_data)

            print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                  str(self.path), str(self.headers), post_data.decode('utf-8'))

            # получаем json
            json_data = json.loads(post_data.decode('utf-8'))
            print('My JSON: ', json_data)
            # отрисовываем графику
            y = logic(json_data)

            # отправляем ответ
            self._set_response(y)


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
    # поднимаем сервер
    run()


if __name__ == "__main__":
    main()
