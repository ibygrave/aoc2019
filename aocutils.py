import aocintcode

def input_ints(input_name):
    with open(input_name) as input_file:
        for input_line in input_file:
            yield int(input_line.strip())

def input_program(input_name, prog_type=aocintcode.Program):
    with open(input_name) as input_file:
        return prog_type(input_file.readline())
