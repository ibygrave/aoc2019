#!/usr/bin/env python

import setuptools

setuptools.setup(name='aoc2019',
      version='1.0',
      description='Advent of Code 2019',
      author='Ian Bygrave',
      author_email='ian@bygrave.me.uk',
      packages=['aoc2019'],
      package_dir={'aoc2019':'src'},
      install_requires=[
          'numpy==1.18.1',
          ],
      )
