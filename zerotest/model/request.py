__author__ = 'Hari Jiang'
import requests


class Request(object):
    def __init__(self, scheme=None, method=None, params=None, url=None, headers=None, data=None):
        self.scheme = scheme
        self.method = method
        self.headers = headers
        self.data = data
        self.params = params
        self.url = url

    def send_request(self):
        return requests.request(self.method, self.url, headers=self.headers,
                                params=self.params, data=self.data,
                                stream=True, allow_redirects=False)
