__author__ = 'Hari Jiang'
from zerotest import utils


def test_dict_to_wsgi_headers():
    data = {"blue": "yellow", "yellow": "red", "red": "blue"}
    assert sorted(utils.dict_to_wsgi_headers(data)) == sorted([("blue", "yellow"), ("yellow", "red"), ("red", "blue")])
