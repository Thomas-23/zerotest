__author__ = 'Hari Jiang'

from zerotest.server import Server
from zerotest.forwarder import Forwarder
from zerotest.tunnel import TraceHTTPTunnel

forwarder = Forwarder('localhost', 5000, tunnel_class=TraceHTTPTunnel)
server = Server(forwarder)

try:
    server.start_serve('', 9090)
except KeyboardInterrupt:
    print "Ctrl C - Stopping server"
finally:
    server.close()

