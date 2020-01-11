#!/usr/bin/python3
import aocintcode

want = 19690720

def read_input_prog():
    with open("day2_input.txt") as input_file:
        for input_line in input_file:
            return aocintcode.Program(input_line)


def search_params(start_prog, want_out):
    for noun in range(100):
        for verb in range(100):
            experiment = aocintcode.Program("", clone=start_prog)
            experiment.mem[1] = noun
            experiment.mem[2] = verb
            try:
                experiment.run()
            except aocintcode.SomethingWentWrong as err:
                continue
            if experiment.mem[0] == want_out:
                print(f"Found noun = {noun}, verb = {verb}")
                return


if __name__ == '__main__':
    start_prog = read_input_prog()
    search_params(start_prog, want)
