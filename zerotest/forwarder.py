__author__ = 'Hari Jiang'

import logging
import socket

LOG = logging.getLogger()


class Forwarder(object):
    def __init__(self, host, port):
        self.up_stream = (host, port)
        self._tunnels_map = {}

    def _new_forward_sock(self):
        forward_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            forward_sock.connect((self.up_stream[0], self.up_stream[1]))
            return forward_sock
        except Exception as e:
            forward_sock.close()
            LOG.exception(e)

    def establish_tunnel(self, client_sock, _client_addr):
        forward_sock = self._new_forward_sock()
        if forward_sock:
            tunnel = Tunnel(forward_sock, client_sock)
            self._tunnels_map[client_sock] = tunnel
            self._tunnels_map[forward_sock] = tunnel
        return forward_sock

    def forward_data(self, sock, data):
        self._tunnels_map[sock].send(sock, data)

    def pop_tunnel_sock(self, sock):
        tunnel = self._tunnels_map[sock]
        sock2 = tunnel.get_pair_sock(sock)
        tunnel.finish(sock)
        del self._tunnels_map[sock]
        del self._tunnels_map[sock2]
        return sock2


class Tunnel(object):
    def __init__(self, server, client):
        self.server = server
        self.client = client

    def send(self, sender_sock, data):
        receiver_sock = self.get_pair_sock(sender_sock)
        receiver_sock.send(data)

    def finish(self, closed_sock):
        pass

    def get_pair_sock(self, sock):
        if self.server == sock:
            return self.client
        elif self.client == sock:
            return self.server

