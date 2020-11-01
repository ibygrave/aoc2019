#!/usr/bin/env python3
from . import aocutils
from . import aocintcode


prog = aocutils.input_program("day5_input.txt")
print(aocintcode.run_test_program(prog))
