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
              'aoc_day1=aoc2019.fuel:day1',
              'aoc_day2=aoc2019.intcode:day2',
              'aoc_day3=aoc2019.wire:day3',
              'aoc_day4=aoc2019.passwordguesser:day4',
              'aoc_day5=aoc2019.intcode:day5',
              'aoc_day6=aoc2019.orbit:day6',
              'aoc_day7=aoc2019.intcode:day7',
              'aoc_day8=aoc2019.sif:day8',
              'aoc_day9=aoc2019.intcode:day9',
              'aoc_day10=aoc2019.asteroids:day10',
              'aoc_day11=aoc2019.ehpr:day11',
              'aoc_day12=aoc2019.gravsim:day12',
              'aoc_day13=aoc2019.breakout:day13',
              'aoc_day14=aoc2019.chem:day14',
              'aoc_day15=aoc2019.repairdroid:day15',
              'aoc_day16=aoc2019.fft:day16',
              ]
          },
      )
