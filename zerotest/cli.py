__author__ = 'Hari Jiang'

import argparse

from zerotest.app import App


DESCRIPTION = """
zerotest command line, manage zerotest server and test generator.
"""

class CLI(object):
    def __init__(self):
        self._parser = None

    def init_arg_parser(self):
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        subparsers = parser.add_subparsers(help='sub-command help')

        start_parser = subparsers.add_parser('start', help='start zerotest service')

        stop_parser = subparsers.add_parser('stop', help='stop zerotest service')

        status_parser = subparsers.add_parser('status', help='zerotest service status')
        self._parser = parser

    def run(self):
        self.init_arg_parser()
        App('', '', '')
