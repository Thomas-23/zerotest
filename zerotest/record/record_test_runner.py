from __future__ import print_function

__author__ = 'Hari Jiang'

import logging

from zerotest.record.formatter import Formatter
from zerotest.response_matcher import ResponseMatcher, MatchError

LOG = logging.getLogger(__name__)


class RecordTestRunner(object):
    """
    run tests from record data
    usage: RecordTestRunner('my_record.data', ignore_headers=['server']).run()
    """

    def __init__(self, record_file, endpoint=None, ignore_headers=None, verify_ssl=False):
        self._record_file = record_file
        self._endpoint = endpoint
        self._verify_ssl = verify_ssl
        self._formatter = Formatter()
        self._response_matcher = ResponseMatcher(ignore_headers=ignore_headers)

    def run(self):
        i = 0
        while True:
            result = self._formatter.read_record(self._record_file)
            if result:
                i += 1
                request, response = result

                # replace request host if set endpoint option
                if self._endpoint:
                    request.endpoint = self._endpoint
                real_response = response.from_requests_response(request.send_request(self._verify_ssl))
                try:
                    self._response_matcher.match_responses(response, real_response)
                except MatchError as e:
                    LOG.error("Test case {} failed: {}".format(i, e))
                    print("---------request---------")
                    print(request)
                    print("-------request end-------")
                    print("\n")
                    print("---------response---------")
                    print(response)
                    print("-------response end-------")
                    break
                else:
                    print(".", end='')
            else:
                print("\n")
                print("Complete all {} test cases.".format(i))
                break
