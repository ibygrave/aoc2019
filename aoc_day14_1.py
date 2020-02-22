#!/usr/bin/python3
import aocchem

with open("day14_input.txt") as input_file:
    factory = aocchem.Factory(input_file)
factory['FUEL'] = -1
factory.reduce()
print(-factory['ORE'])
