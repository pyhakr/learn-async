import socket
from queue import Queue

q = Queue()

def parse_links(page):
    return 'foo'

def fetch(url):
    sock = socket.socket()
    sock.connect((url, 80))
    request = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(url)
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)

    # Page is now downloaded.
    links = parse_links(response)
    q.add(links)


fetch('xkcd.com')