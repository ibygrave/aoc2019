#!/usr/bin/env python3
import aocutils
import aocintcode


with open("day7_input.txt") as input_file:
    prog = input_file.readline()

phases = [5, 6, 7, 8, 9]
print(aocintcode.optimize_amps(prog, phases, aocintcode.feedback_control_amps))
