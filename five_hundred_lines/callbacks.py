import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


urls_todo = set(['/'])
seen_urls = set(['/'])
selector = DefaultSelector()



class Fetcher:
    def __init__(self, url):
        self.response = b''  # Empty array of bytes.
        self.url = url
        self.sock = None

    def parse_links(self):
        # TODO: implement parse links
        print('parse_links called')
        return set(['/'])

    # Method on Fetcher class.
    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('xkcd.com', 80))
        except BlockingIOError:
            pass

        # Register next callback.
        selector.register(self.sock.fileno(),
                          EVENT_WRITE,
                          self.connected)

    # Method on Fetcher class.
    def connected(self, key, mask):
        print('connected!')
        selector.unregister(key.fd)
        #TODO: get the request format right to return page
        request = 'GET {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(self.url)
        self.sock.send(request.encode('ascii'))

        # Register the next callback.
        selector.register(key.fd,
                          EVENT_READ,
                          self.read_response)

    # Method on Fetcher class.
    def read_response(self, key, mask):
        global stopped

        chunk = self.sock.recv(4096)  # 4k chunk size.
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)  # Done reading.
            links = self.parse_links()

            # Python set-logic:
            for link in links.difference(seen_urls):
                urls_todo.add(link)
                Fetcher(link).fetch()  # <- New Fetcher.

            seen_urls.update(links)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True


# Begin fetching http://xkcd.com/353/
fetcher = Fetcher('https://xkcd.com/353/')
fetcher.fetch()


stopped = False


def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            print('EVENT CAUGHT: {%s}' % event_key.data.__func__)
            callback = event_key.data
            callback(event_key, event_mask)

loop()