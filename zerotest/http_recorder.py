__author__ = 'Hari Jiang'

from Queue import Queue, Empty
import threading
import logging

from zerotest.tunnel import Tunnel
from zerotest.common import HTTP_LINE_BREAK


LOG = logging.getLogger(__name__)


class HTTPRecorder(object):
    """
    format and record tunnel request/response to file
    """

    def __init__(self, filepath):
        """
        :param filepath: new record will append to file if filepath exists
        :return:
        """
        self.filepath = filepath
        self._running = False
        self._closing = False
        self._service_thread = None
        self._queue = Queue()

    def start_service(self):
        """
        start recorder service
        :return:
        """
        self._service_thread = threading.Thread(target=self._loop_work)
        self._running = True
        self._service_thread.start()
        LOG.debug("recorder service start")

    def _loop_work(self):
        record_file = open(self.filepath, "a+b")
        while True:
            tunnel = self._queue.get()
            LOG.debug("receive tunnel %s", tunnel)
            if tunnel is None:
                record_file.close()
                return
            request_bytes = len(tunnel.request)
            response_bytes = len(tunnel.response)
            record_file.write("{},{},{}".format(request_bytes + response_bytes, request_bytes, response_bytes))
            record_file.write("\n")
            record_file.write(tunnel.request)
            record_file.write(tunnel.response)
            record_file.write("\n")

    def record_tunnel(self, tunnel):
        """
        async method, put tunnel into task queue
        :param tunnel:
        :return:
        """
        if not self._closing:
            assert isinstance(tunnel, Tunnel)
            LOG.debug("record tunnel %s", tunnel)
            self._queue.put(tunnel)

    def close(self):
        """
        graceful close, wait util queue empty
        :return:
        """
        if self._running:
            LOG.debug("closing...")
            self._closing = True
            self._queue.put(None)
            LOG.debug("wait task complete...")
            self._service_thread.join()
        else:
            raise RuntimeError("current service is not running")

    def shutdown(self):
        """
        shutdown service, threw out items already in queue
        :return:
        """
        LOG.debug("shutdown...")
        self._closing = True
        try:
            while True:
                self._queue.get_nowait()
        except Empty:
            pass

        self.close()