__author__ = 'Hari Jiang'


class Formatter(object):
    def __init__(self):
        self._delimiter = "\n"

    def write_record(self, writeable, request, response):
        writeable.write(self.encode_metadata(request, response))
        writeable.write(self._delimiter)
        writeable.write(request)
        writeable.write(response)
        writeable.write(self._delimiter)

    def read_record(self, readable):
        _, request_bytes, response_bytes = self.decode_metadata(readable.readline())
        request = readable.read(request_bytes)
        response = readable.read(response_bytes)
        readable.readline()
        return request, response

    def encode_metadata(self, request, response):
        assert isinstance(request, bytearray)
        assert isinstance(response, bytearray)
        request_bytes = len(request)
        response_bytes = len(response)
        return "{},{},{}".format(request_bytes + response_bytes, request_bytes, response_bytes)

    def decode_metadata(self, metadata):
        total_bytes, request_bytes, response_bytes = map(int, metadata.strip(self._delimiter).split(','))
        return total_bytes, request_bytes, response_bytes
