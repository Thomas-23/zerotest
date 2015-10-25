__author__ = 'Hari Jiang'

import logging
import socket
import select
import time


logging.basicConfig()
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)


# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
BUFFER_SIZE = 4096
WAIT_READABLE_SECONDS = 0.0001


class Forwarder():

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
            self._tunnels_map[client_sock] = forward_sock
            self._tunnels_map[forward_sock] = client_sock
        return forward_sock

    def forward_data(self, sock, data):
        self._tunnels_map[sock].send(data)

    def pop_tunnel_sock(self, sock):
        sock2 = self._tunnels_map[sock]
        del self._tunnels_map[sock]
        del self._tunnels_map[sock2]
        return sock2


class Server():

    def __init__(self):
        self.incoming = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.forwarder = Forwarder('localhost', 5000)

    def start_serve(self, host, port):
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
                    else:
                        self.on_recv(r, data)
                else:
                    time.sleep(WAIT_READABLE_SECONDS)
            except StandardError as e:
                print e

    def on_accept(self):
        client_sock, client_addr = self.server.accept()
        forward_sock = self.forwarder.establish_tunnel(client_sock, client_addr)
        if forward_sock:
            print client_addr, "has connected"
            self.incoming.append(client_sock)
            self.incoming.append(forward_sock)
        else:
            print "Can't establish connection with remote server.",
            print "Closing connection with client side", client_addr
            client_sock.close()

    def on_close(self, sock):
        print sock.getpeername(), "has disconnected"
        tunnel_sock = self.forwarder.pop_tunnel_sock(sock)
        self.incoming.remove(sock)
        self.incoming.remove(tunnel_sock)
        sock.close()
        tunnel_sock.close()

    def on_recv(self, sock, data):
        # here we can parse and/or modify the data before send forward
        print data
        self.forwarder.forward_data(sock, data)

    def close(self):
        self.server.close()

if __name__ == '__main__':
        server = Server()
        try:
            server.start_serve('', 9090)
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
        finally:
            server.server.close()

