__author__ = 'Hari Jiang'

import argparse
import sys
from urlparse import urlparse
import os
import logging
import tempfile

DESCRIPTION = """
zerotest command line, manage zerotest server and test generator.
"""

if os.getenv('ZEROTEST_DEBUG'):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)


class CLI(object):
    def __init__(self):
        self._parser = None
        self._parse_result = None

    def _init_arg_parser(self):
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')

        server_parser = subparsers.add_parser('server', help='start zerotest local proxy server')
        server_parser.add_argument('url', help="target url: http://example.com")
        server_parser.add_argument('-f', '--file', help="file path to store record, default: [random path]")
        server_parser.add_argument('-b', '--bind', help="local bind address, default: 127.0.0.1")
        server_parser.add_argument('-p', '--port', help="local port, default: [random port]")

        run_parser = subparsers.add_parser('run', help='run record file test')
        run_parser.add_argument('file', help="zerotest record file")

        self._parser = parser

    def run(self, argv=sys.argv[1:]):
        self._init_arg_parser()
        self._parse_result = self._parser.parse_args(argv)
        getattr(self, 'command_{}'.format(self._parse_result.subparser_name))()

    def exit_with_error_message(self, message):
        LOG.error(message)
        exit(1)

    def command_server(self):
        """
        sub-command start
        :return:
        """
        from zerotest.app import App

        url = self._parse_result.url
        parsed_url = urlparse(url)
        forward_host = parsed_url.hostname
        forward_port = parsed_url.port or 80
        if not forward_host:
            self.exit_with_error_message("invalid url '{}'".format(url))

        filepath = self._parse_result.file

        if not filepath:
            _, filepath = tempfile.mkstemp()
        else:
            if os.path.exists(filepath):
                LOG.warning("file '{}' is exists, new record will append to the file".format(filepath))

        app = App(forward_host, forward_port, filepath)
        host = self._parse_result.bind or '127.0.0.1'
        port = int(self._parse_result.port or 3000)
        try:
            app.start(host, port)
        except KeyboardInterrupt:
            LOG.info("closing atpp...")
            app.close()

    def command_run(self):
        """
        sub-command run
        run record file
        :return:
        """
        from zerotest.record.record_test_runner import RecordTestRunner

        filepath = self._parse_result.file
        if not os.path.exists(filepath):
            LOG.warning("file '{}' not exists".format(filepath))

        with open(filepath, 'r') as f:
            RecordTestRunner(f).run()
