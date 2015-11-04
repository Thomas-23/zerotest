__author__ = 'Hari Jiang'

import json
from zerotest.model.request import Request
from zerotest.model.response import Response


class Formatter(object):
    def write_record(self, writeable, request, response):
        record = dict(request=request.__dict__, response=response.__dict__)
        writeable.write(json.dumps(record))
        writeable.write("\n")

    def read_record(self, readable):
        line = readable.readline()
        record = json.loads(line)
        request = Request()
        request.__dict__.update(record['request'])
        response = Response()
        response.__dict__.update(record['response'])
        return request, response
