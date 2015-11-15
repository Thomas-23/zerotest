# ZEROTEST [![PyPI](https://img.shields.io/pypi/v/zerotest.svg)](https://pypi.python.org/pypi/zerotest) [![Travis](https://img.shields.io/travis/jjyr/zerotest.svg)](https://travis-ci.org/jjyr/zerotest)

Zerotest makes it easy to test API server, start a micro proxy, send requests, and generate test code by these behaviours.

> *Zerotest makes test api server like a boss!*

## Install
Stable version: `pip install zerotest`

Develop version: `pip install git+https://github.com/jjyr/zerotest.git`

## Usage
1. Start a local proxy to capture http traffic `zerotest server https://api.github.com -f octocat.data`

2. Make few requests `curl -i http://localhost:7000/users/octocat`

3. Press `C-c` to exit local proxy

4. Generate test code `zerotest generate octocat.data --ignore-all-headers > test_octocat.py`

5. Type `py.test test_octocat.py` to run test

## Contribute
* Open issue if found bugs or some cool ideas
* Feel free to ask if have any questions
* Testing is very important for a test tool, commit your test file together with pull request
