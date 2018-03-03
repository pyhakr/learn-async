import re
import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


urls_todo = set(['/feeds/lists.shtml'])
seen_urls = set(['/feeds/lists.shtml'])
url_link_map = {}
url_new_link_map = {}

selector = DefaultSelector()

class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        print("setting Future result to: {}".format(result))
        self.result = result
        for fn in self._callbacks:
            print("calling callback: {}".format(fn))
            fn(self)

class Task:
    """
    1. set Task co-routine to be passed in function
    2. create Future, set result to None
    3. call step which sends future result to co-routine

    each time the co-routine yields a future
     - we add Task.step to the future callback list
     - when event loop triggers inner on_connected function of co-routine
     - the future is resolved and Task.step is called again
    """
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            print('Sending Future.result to co-routine')
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        print('got next future from co-routine, adding step to call back list')
        next_future.add_done_callback(self.step)


class Fetcher:
    def __init__(self, url):
        self.response = b''  # Empty array of bytes.
        self.url = url
        self.sock = None

    # 2. Then fetch runs until it yields a future, which the task captures as next_future
    def fetch(self):
        global stopped
        print("*** fetch runs until it yields a future ***")
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('www.uen.org', 80))
        except BlockingIOError:
            pass

        f = Future()

        def on_connected():
            print("*** socket connected: clearing future result *** ")
            f.set_result(None)
            # print('connected: %s' % self.url)
            # selector.unregister(key.fd)
            request = 'GET {} HTTP/1.1\r\nHost: www.uen.org\r\n\r\n'.format(self.url)
            sock.send(request.encode('utf-8'))


        # Register next callback.
        selector.register(sock.fileno(),EVENT_WRITE, on_connected)

        print("*** yield future to Task ***")
        # yield f
        self.response = yield from read_all(sock)

        selector.unregister(sock.fileno())
        print('connected!')

stopped = False


def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            # print('EVENT CAUGHT: {%s}' % event_key.data.__func__)
            callback = event_key.data
            # callback(event_key, event_mask)
            callback()


def read(sock):
    f = Future()

    def on_readable():
        f.set_result(sock.recv(4096))

    selector.register(sock.fileno(), EVENT_READ, on_readable)
    print("READING: yielding future to Task")
    chunk = yield f
    selector.unregister(sock.fileno())
    return chunk


def read_all(sock):
    response = []
    chunk = yield from read(sock)
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)
    return b''.join(response)


fetcher = Fetcher('/feeds/lists.shtml')
# 1. starts the fetch generator by sending None into it.
print('*** fetch generator started ***')
Task(fetcher.fetch())
loop()







