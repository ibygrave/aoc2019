#!/usr/bin/python3
from . import aocorbit

with open("day6_input.txt") as input_file:
    print(aocorbit.count_orbits(input_file))
