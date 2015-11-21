"""
proxy of zerotest proxy server
"""

import tempfile
import time
from subprocess import Popen
from urlparse import urljoin

import requests

from tests.mock import pickup_port


class Proxy(object):
    def __init__(self):
        self.port = None
        self._process = None
        _, self.data_file = tempfile.mkstemp()

    @property
    def url(self):
        return 'http://127.0.0.1:{}'.format(self.port)

    @property
    def running(self):
        if not self._process:
            return False
        self._process.poll()
        return not self._process.returncode

    def shutdown(self):
        if self.running:
            self._process.kill()

    def start_server(self, url):
        """
        :param url: tested server
        :return:
        """
        port = pickup_port()
        self._process = Popen(['python', 'zerotest/cli.py', 'server', '-p', str(port), '-f', self.data_file, url])
        self.port = port
        test_count = 10
        while test_count > 0:
            try:
                if self.running:
                    r = requests.get(urljoin(self.url, '/count'))
                    if r.status_code == 200:
                        return
            except requests.exceptions.ConnectionError:
                pass

            print("wait proxy start,", test_count)
            time.sleep(1)
            test_count -= 1
        else:
            self.shutdown()
            raise RuntimeError("start zerotest proxy timeout")
