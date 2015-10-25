__author__ = 'Hari Jiang'

from zerotest.server import Server
from zerotest.forwarder import Forwarder

forwarder = Forwarder('localhost', 5000)
server = Server(forwarder)
try:
    server.start_serve('', 9090)
except KeyboardInterrupt:
    print "Ctrl C - Stopping server"
finally:
    server.close()

