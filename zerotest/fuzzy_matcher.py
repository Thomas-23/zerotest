from __future__ import unicode_literals


class FuzzyMatcher(object):
    def __init__(self):
        self._content1 = None
        self._content2 = None

    def set_items(self, content1, content2):
        assert isinstance(content1, dict)
        assert isinstance(content2, dict)
        self._content1 = content1
        self._content2 = content2
