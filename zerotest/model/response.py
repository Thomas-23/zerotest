__author__ = 'Hari Jiang'


class Response(object):
    def __init__(self, status=None, headers=None, body=None):
        self.status = status
        self.headers = headers
        self.body = body
