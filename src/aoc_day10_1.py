#!/usr/bin/python3
from . import aocasteroids

with open("day10_input.txt") as input_file:
    am = aocasteroids.AsteroidMap(input_file)
print(am.best_monitor().detects)
