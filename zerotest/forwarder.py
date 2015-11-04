__author__ = 'Hari Jiang'

import logging
from urlparse import urljoin

import werkzeug.wrappers

from zerotest.utils import response_with_response
from zerotest.model.request import Request
from zerotest.model.response import Response

LOG = logging.getLogger(__name__)


class Forwarder(object):
    def __init__(self, forward_url):
        self._forward_url = forward_url
        self._on_forward_complete_callbacks = []

    def __call__(self, environ, start_response):
        # pop incorrect content length, I don't know why
        environ.pop('CONTENT_LENGTH', None)
        request = werkzeug.wrappers.Request(environ)

        # remove Host from request headers, then set X-Forwarded-Host
        headers = {k: v for k, v in request.headers if k not in ('Host',)}
        # headers['X-FORWARDED-HOST'] = request.headers['HOST']
        LOG.debug("forward to [%s]%s, headers: -----%s-----", request.method, self._forward_url, headers)
        url = urljoin(self._forward_url, request.path)
        request_model = Request(scheme=request.scheme, method=request.method, headers=headers, data=request.data,
                                params=request.query_string, url=url)
        response = request_model.send_request()
        response_model = Response(status=response.status_code, body=response.text,
                                  headers=dict(response.headers))
        self.trigger_on_forward_complete(request_model, response_model)
        return response_with_response(response, start_response)

    def on_forward_complete(self, callback):
        self._on_forward_complete_callbacks.append(callback)

    def trigger_on_forward_complete(self, request, response):
        for callback in self._on_forward_complete_callbacks:
            callback(request, response)
