"""
A commandline command (Python3 program) that compares two (CSV) statistics with each other and generates delta values from the (old and the new) values.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='statsdelta',
      version='0.0.1',
      description='a commandline command (Python3 program) that compares two (CSV) statistics with each other and generates delta values from the (old and the new) values',
      url='https://github.com/slub/statsdelta',
      author='Bo Ferri',
      author_email='zazi@smiy.org',
      license="Apache 2.0",
      packages=[
          'statsdelta',
      ],
      package_dir={'statsdelta': 'statsdelta'},
      install_requires=[
          'argparse>=1.4.0'
      ],
      entry_points={
          "console_scripts": ["statsdelta=statsdelta.statsdelta:run"]
      }
      )
