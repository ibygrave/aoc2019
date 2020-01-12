#!/usr/bin/python3
import aocutils
import aocintcode

want = 19690720

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
    start_prog = aocutils.input_program("day2_input.txt")
    search_params(start_prog, want)
