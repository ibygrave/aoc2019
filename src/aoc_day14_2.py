#!/usr/bin/python3
from . import aocchem

with open("day14_input.txt") as input_file:
    factory = aocchem.Factory(input_file)
print(aocchem.fuel_given_ore(
    factory, ore_budget=1000000000000))
