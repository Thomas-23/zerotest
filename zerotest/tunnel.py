__author__ = 'Hari Jiang'


class Tunnel(object):
    def __init__(self, server, client):
        self.server = server
        self.client = client
        self.closed_sock = None

    def send(self, sender_sock, data):
        receiver_sock = self.get_pair_sock(sender_sock)
        receiver_sock.send(data)

    def finish(self, closed_sock):
        self.closed_sock = closed_sock

    def get_pair_sock(self, sock):
        if self.server == sock:
            return self.client
        elif self.client == sock:
            return self.server


class TraceHTTPTunnel(Tunnel):
    def __init__(self, *args, **kwargs):
        super(TraceHTTPTunnel, self).__init__(*args, **kwargs)
        self.request = bytearray()
        self.response = bytearray()

    def send(self, sender_sock, data):
        if sender_sock == self.server:
            self.client.send(data)
            self.response += data
        elif sender_sock == self.client:
            self.server.send(data)
            self.request += data
        else:
            raise LookupError("sender_sock not found in this tunnel")

    def finish(self, closed_sock):
        super(TraceHTTPTunnel, self).finish(closed_sock)
        print "finish by client:", closed_sock == self.client
        print "-----request-------"
        print self.request
        print "-----response-------"
        print self.response
