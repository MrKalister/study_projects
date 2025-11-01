import socket
import time
import views


URLS = {
    '/': views.index,
    '/blog': views.blog
}


def parse_request(request):
    '''Parse request and take method and url from this.'''

    method, url = None, None
    try:
        parsed = request.split(' ')
        method, url = parsed[0], parsed[1]
    except IndexError:
        time.sleep(3)
        parsed = request.split(' ')
        method, url = parsed[0], parsed[1]
    finally:
        return (method, url)


def generate_headers(method, url):
    '''Check method and url and return headers.'''

    if method != 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)
    if url not in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)
    return ('HTTP/1.1 200 OK\n\n', 200)


def generate_content(code, url):
    '''Return content depending on the code.'''

    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    return URLS[url]()


def generate_response(request):
    '''Consolidate and return response.'''

    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = generate_content(code, url)
    # сокеты принимают только байты, поэтому строку кодируем в байты.
    return (headers + body).encode()


def run():
    # AF_INET это протокол IP адреса 4 версии
    # SOCK_STREAM это протокол TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Чтобы отключить защитный механизм, который блокирует недавно
    # используемый порт примерно на 1.5 минуты, что бы все данные
    # были успешно получены. Передаем следующие аргументы:
    # сам текущий сокет, название параметра, 1 - как значение True.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # связать субъект с конкретным адресом и портом
    server_socket.bind(('localhost', 5000))
    # чтобы сервер слушал этот порт.
    server_socket.listen()
    # Создаем бесконечный цикл, т.к. получать запросы 
    # и отдавать ответы - это бесконечный процесс
    while True:
        # получаем сокет и адрес клиента, который обратился на наш сервер
        client_socket, addr = server_socket.accept()
        # количество байт в пакете, которые будем получать от клиента
        request = client_socket.recv(1024)
        # print(request.decode('utf-8'))
        print(request)
        print()
        print(addr)
        response = generate_response(request.decode('utf-8'))
        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    run()
