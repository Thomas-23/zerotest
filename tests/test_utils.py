__author__ = 'Hari Jiang'
from zerotest.utils import wsgi_helper


def test_dict_to_wsgi_headers():
    data = {"blue": "yellow", "yellow": "red", "red": "blue"}
    assert sorted(wsgi_helper.dict_to_wsgi_headers(data)) == sorted([("blue", "yellow"), ("yellow", "red"), ("red", "blue")])
