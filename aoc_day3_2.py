#!/usr/bin/python3
import aocwire

with open("day3_input.txt") as input_file:
    w1 = aocwire.Wire(input_file.readline())
    w2 = aocwire.Wire(input_file.readline())

print(w1.steps_first_cross(w2))
