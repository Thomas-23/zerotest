__author__ = 'Hari Jiang'

import logging
import socket
from zerotest.tunnel import Tunnel

LOG = logging.getLogger()


class Forwarder(object):
    def __init__(self, host, port, tunnel_class=Tunnel):
        self.up_stream = (host, port)
        self._tunnels_map = {}
        assert issubclass(tunnel_class, Tunnel)
        self._tunnel_class = tunnel_class

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
            tunnel = self._tunnel_class(forward_sock, client_sock)
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


