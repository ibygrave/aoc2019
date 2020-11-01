#!/usr/bin/python3
from . import aocgravsim

with open("day12_input.txt") as input_file:
    ms = aocgravsim.MoonSim(input_file)
ms.step(nsteps=1000)
print(ms.total_energy())
