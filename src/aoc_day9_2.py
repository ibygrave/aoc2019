#!/usr/bin/env python3
from . import aocutils
from . import aocintcode


prog = aocutils.input_program("day9_input.txt")
print(aocintcode.run_test_program(prog, system_ids=[2]))
