#!/usr/bin/env python

from distutils.core import setup

setup(name='zerotest',
      version='0.0.0',
      description='Capture HTTP request/response and replay it for the test purpose',
      author='Hari Jiang',
      author_email='hari.jiang@outlook.com',
      scripts=['scripts/zerotest'],
      packages=['zerotest'],
      requires=[
          'requests>=2.2.1',
          'Werkzeug>=0.10.4',
      ]
      )
