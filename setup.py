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
      entry_points = {
          'console_scripts': [
              'aoc_day1=aoc2019.aocfuel:day1',
              'aoc_day2=aoc2019.aocintcode:day2',
              'aoc_day3=aoc2019.aocwire:day3',
              'aoc_day4=aoc2019.aocpasswordguesser:day4',
              'aoc_day5=aoc2019.aocintcode:day5',
              'aoc_day6=aoc2019.aocorbit:day6',
              'aoc_day7=aoc2019.aocintcode:day7',
              'aoc_day8=aoc2019.aocsif:day8',
              'aoc_day9=aoc2019.aocintcode:day9',
              'aoc_day10=aoc2019.aocasteroids:day10',
              'aoc_day11=aoc2019.aocehpr:day11',
              'aoc_day12=aoc2019.aocgravsim:day12',
              'aoc_day13=aoc2019.aocbreakout:day13',
              'aoc_day14=aoc2019.aocchem:day14',
              'aoc_day15=aoc2019.aocrepairdroid:day15',
              'aoc_day16=aoc2019.aocfft:day16',
              ]
          },
      )
