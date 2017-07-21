import socket
from queue import Queue

q = Queue()

def parse_links(page):
    return 'foo'

def fetch(url):
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect((url, 80))
    except BlockingIOError as e:
        print(e.args)
        pass
    request = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(url)
    while True:
        try:
            sock.send(request.encode('ascii'))
            break  # Done.
        except OSError as e:
            pass

    print('sent')
    response = b''
    try:
        chunk = sock.recv(4096)
        while chunk:
            response += chunk
            chunk = sock.recv(4096)
    except BlockingIOError as e:
        print(e.args)
    # Page is now downloaded.
    links = parse_links(response)
    q.put(links)


fetch('xkcd.com')