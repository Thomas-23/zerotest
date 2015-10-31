__author__ = 'Hari Jiang'

import logging
import socket
import select
import time


LOG = logging.getLogger(__name__)


BUFFER_SIZE = 4096
WAIT_READABLE_SECONDS = 0.0001


class Server():

    def __init__(self, forwarder):
        self.incoming = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.forwarder = forwarder

    def start_serve(self, host, port):
        LOG.info("local proxy server start on {}:{}".format(host, port))
        self.server.bind((host, port))
        self.server.listen(300)

        self.incoming.append(self.server)
        while True:
            try:
                reads, writes, excepts = select.select(self.incoming, [], [])
                for r in reads:
                    if r == self.server:
                        self.on_accept()
                        break

                    data = r.recv(BUFFER_SIZE)
                    if len(data) == 0:
                        self.on_close(r)
                        break
                    else:
                        self.on_recv(r, data)
                else:
                    time.sleep(WAIT_READABLE_SECONDS)
            except StandardError as e:
                LOG.error(e)

    def on_accept(self):
        client_sock, client_addr = self.server.accept()
        LOG.debug("accept client %s", client_addr)
        forward_sock = self.forwarder.establish_tunnel(client_sock, client_addr)
        if forward_sock:
            LOG.debug("%s has connected", client_addr)
            self.incoming.append(client_sock)
            self.incoming.append(forward_sock)
        else:
            LOG.info("Can't establish connection with remote server.")
            LOG.debug("Closing connection with client side %s", client_addr)
            client_sock.close()

    def on_close(self, sock):
        LOG.debug("%s has disconnected", sock.getpeername())
        tunnel_sock = self.forwarder.pop_tunnel_sock(sock)
        self.incoming.remove(sock)
        self.incoming.remove(tunnel_sock)
        sock.close()
        tunnel_sock.close()

    def on_recv(self, sock, data):
        self.forwarder.forward_data(sock, data)

    def close(self):
        self.server.close()
        LOG.info("server closed")
