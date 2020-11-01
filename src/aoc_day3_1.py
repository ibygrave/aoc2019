#!/usr/bin/python3
from . import aocwire

with open("day3_input.txt") as input_file:
    w1 = aocwire.Wire(input_file.readline())
    w2 = aocwire.Wire(input_file.readline())

print(w1.distance_closest_cross(w2))
