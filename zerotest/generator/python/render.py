"""
test renderer of python
"""

from jinja2 import Template

__author__ = 'Hari Jiang'


class Renderer(object):
    def __init__(self, options, match_options):
        self.options = options
        self.match_options = match_options

    def prepare(self, records):
        pass

    def render(self, records):
        self.prepare(records)
        t = Template(_TEMPLATE)
        result = t.render(match_options=self.match_options, records=records)
        return result


_TEMPLATE = """
from zerotest.response_matcher import ResponseMatcher, MatchError

matcher = ResponseMatcher(**{{match_options}})


def test_response__str__():
    response = Response(200, {"just test": "hope pass"}, "happy test!")
    assert str(response) == ""

"""
