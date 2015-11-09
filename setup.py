#!/usr/bin/env python

import sys

from setuptools import find_packages, setup
from setuptools.command.test import test


class PyTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name='zerotest',
      version='0.0.0',
      description='Capture HTTP request/response and replay it for the test purpose',
      author='Hari Jiang',
      author_email='hari.jiang@outlook.com',
      license='MIT',
      cmdclass={'test': PyTest},
      packages=find_packages(),
      install_requires=[
          'requests>=2.2.1',
          'Werkzeug>=0.10.4',
      ],
      tests_require=[
          'pytest>=2.8.2',
      ],
      entry_points={
          'console_scripts': [
              'zerotest=zerotest.cli:main',
          ],
      },
      )
