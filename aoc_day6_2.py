#!/usr/bin/python3
import aocorbit

omap = aocorbit.OrbitMap()
with open("day6_input.txt") as input_file:
    omap.input_orbits(input_file)
omap.count_orbits()
print(len(omap.plan_route("YOU", "SAN"))-1)
