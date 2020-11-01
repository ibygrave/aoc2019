#!/usr/bin/env python3
from . import aocutils
from . import aocintcode
from . import aocehpr


prog = aocutils.input_program("day11_input.txt")
ehpr = aocehpr.Robot(prog)
ehpr.run()
print(ehpr.count_painted())
