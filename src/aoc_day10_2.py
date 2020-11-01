#!/usr/bin/python3
from . import aocasteroids

with open("day10_input.txt") as input_file:
    am = aocasteroids.AsteroidMap(input_file)
ims = am.best_monitor()
v = am.vaporize(ims.x, ims.y)
for _ in range(199):
    next(v)
cc = next(v)  # 200th
print(100 * cc.x + cc.y)
