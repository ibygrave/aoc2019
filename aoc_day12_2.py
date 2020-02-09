#!/usr/bin/python3
import aocgravsim

with open("day12_input.txt") as input_file:
    ms = aocgravsim.MoonSim(input_file)
print(ms.repeat_period())
