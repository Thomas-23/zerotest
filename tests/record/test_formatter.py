__author__ = 'Hari Jiang'
from StringIO import StringIO

from zerotest.record.formatter import Formatter
from zerotest.request import Request
from zerotest.response import Response

req = Request(scheme="http", method="get", params="query_string=here", host="example.com", path="/test",
              headers={"just": "header"}, data="request")
res = Response(status=200, headers={"responsed": "header"}, body="response")
formatter = Formatter()

dumped = """{"request": {"headers": {"just": "header"}, "host": "example.com", "params": "query_string=here", "path": "/test", "scheme": "http", "data": "request", "method": "get"}, "response": {"status": 200, "headers": {"responsed": "header"}, "body": "response"}}
"""


def test_write():
    writable = StringIO()
    formatter.write_record(writable, req, res)
    assert writable.getvalue() == dumped


def test_read():
    readable = StringIO(dumped)
    request, response = formatter.read_record(readable)
    assert req.__dict__ == request.__dict__
    assert res.__dict__ == response.__dict__
