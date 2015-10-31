__author__ = 'Hari Jiang'

from zerotest.server import Server
from zerotest.forwarder import Forwarder
from zerotest.tunnel import TraceHTTPTunnel
from zerotest.record.http_recorder import HTTPRecorder


class App(object):
    def __init__(self, forward_host, forward_port, record_file_path):
        forwarder = Forwarder(forward_host, forward_port, tunnel_class=TraceHTTPTunnel)
        self.server = Server(forwarder)
        self.recorder = HTTPRecorder(record_file_path)
        forwarder.set_tunnel_close_callback(lambda t, _: self.recorder.record_tunnel(t))

    def start(self, host, port):
        self.recorder.start_service()
        try:
            self.server.start_serve(host, port)
        except:
            self.recorder.close()
            raise

    def close(self):
        self.server.close()
        self.recorder.close()
