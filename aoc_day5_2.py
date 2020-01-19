#!/usr/bin/env python3
import aocutils
import aocintcode


prog = aocutils.input_program("day5_input.txt")
print(aocintcode.run_test_program(prog, system_ids=[5]))
