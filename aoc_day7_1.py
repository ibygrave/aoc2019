#!/usr/bin/env python3
import aocutils
import aocintcode


with open("day7_input.txt") as input_file:
    prog = input_file.readline()

phases = [0, 1, 2, 3, 4]
print(aocintcode.optimize_amps(prog, phases, aocintcode.control_amps))
