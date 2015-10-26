__author__ = 'Hari Jiang'

from zerotest.server import Server
from zerotest.forwarder import Forwarder
from zerotest.tunnel import TraceHTTPTunnel
from zerotest.http_recorder import HTTPRecorder

forwarder = Forwarder('localhost', 5000, tunnel_class=TraceHTTPTunnel)
server = Server(forwarder)
recorder = HTTPRecorder("./test.data")
recorder.start_service()


def handler(tunnel, _):
    recorder.record_tunnel(tunnel)

forwarder.set_tunnel_close_callback(handler)

try:
    server.start_serve('', 9090)
except KeyboardInterrupt:
    print "Ctrl C - Stopping server"
finally:
    server.close()
    recorder.close()

