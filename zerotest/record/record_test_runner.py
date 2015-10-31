__author__ = 'Hari Jiang'

import requests
from zerotest.record.formatter import Formatter


class RecordTestRunner(object):
    def __init__(self, record_file):
        self._record_file = record_file
        self._formatter = Formatter()

    def run(self):
        raw_request, raw_response = self._formatter.read_record(self._record_file)
        print raw_request, raw_response
