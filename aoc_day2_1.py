#!/usr/bin/python3
import aocintcode

with open("day2_input.txt") as input_file:
    for input_line in input_file:
        prog = aocintcode.Program(input_line)
        prog.mem[1] = 12
        prog.mem[2] = 2
        print("IN:", prog)
        prog.run()
        print("OUT:", prog)
