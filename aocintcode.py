
class SomethingWentWrong(Exception):
    pass


class Halt(Exception):
    pass

class Program(object):
    def __init__(self, init, clone=None):
        if clone is not None:
            self.mem = clone.mem[:]
        else:
            self.mem = list(map(int, init.strip().split(',')))
        self.pc = 0
    def binary_math_op(self, fn):
        in1_addr = self.mem[self.pc + 1]
        in2_addr = self.mem[self.pc + 2]
        out_addr = self.mem[self.pc + 3]
        in1 = self.mem[in1_addr]
        in2 = self.mem[in2_addr]
        self.mem[out_addr] = fn(in1, in2)
    def do_opcode_99(self):
        raise Halt()
    def do_opcode_1(self):
        self.binary_math_op(lambda x, y: x+y)
    def do_opcode_2(self):
        self.binary_math_op(lambda x, y: x*y)
    def step(self):
        try:
            opcode = self.mem[self.pc]
            do_opcode = getattr(self, f"do_opcode_{opcode}")
        except (IndexError, AttributeError) as err:
            raise SomethingWentWrong() from err
        do_opcode()
        self.pc += 4
    def run(self):
        try:
            while True:
                self.step()
        except Halt as err:
            pass
    def __str__(self):
        return ','.join(str(x) for x in self.mem)
