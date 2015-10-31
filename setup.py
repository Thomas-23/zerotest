#!/usr/bin/env python

from distutils.core import setup

setup(name='zerotest',
      version='0.0.0',
      description='Generator integrated test for web app with zero lines code need to write',
      author='Hari Jiang',
      author_email='hari.jiang@outlook.com',
      scripts=['scripts/zerotest'],
      packages=['zerotest'],
      requires=['requests>=2.2.1']
      )
