import socket
import threading
from time import sleep
from queue import Queue
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

q = Queue()
selector = DefaultSelector()


def parse_links(page):
    return 'foo'

def loop():
    while True:
        events = selector.select()
        for event_key, event_mask in events:
            print('{}: {}'.format(event_key, event_key.data))
            callback = event_key.data
            callback()

def fetch(url):
    sock = socket.socket()
    sock.setblocking(False)

    try:
        sock.connect((url, 80))
    except BlockingIOError as e:
        print(e.args)

    print('fetching: {}'.format(url))

    def connected():
        selector.unregister(sock.fileno())
        print('connected!')

    selector.register(sock.fileno(), EVENT_WRITE, connected)

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

urls = ['xkcd.com', 'foxnews.com', 'cnn.com']

# fetch_thread = threading.Thread(target=fetch, args=(url,))
# fetch_thread.start()

event_thread = threading.Thread(target=loop)
event_thread.start()

while True:
    for url in urls:
        fetch(url)
    sleep(5)
