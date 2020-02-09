#!/usr/bin/env python3
import aocutils
import aocintcode
import aocehpr


prog = aocutils.input_program("day11_input.txt")
ehpr = aocehpr.Robot(prog)
ehpr.painted[(0, 0)] = 1
ehpr.run()
print(ehpr)
