#!/usr/bin/python3
import aocutils
import aocintcode

prog = aocutils.input_program("day2_input.txt")
prog.mem[1] = 12
prog.mem[2] = 2
prog.run()
print(prog.mem[0])
