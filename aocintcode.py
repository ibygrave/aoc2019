
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
    def param(self, param_ix):
        return self.mem[self.pc + param_ix]
    def binary_math_op(self, fn):
        in1_addr = self.param(1)
        in2_addr = self.param(2)
        out_addr = self.param(3)
        in1 = self.mem[in1_addr]
        in2 = self.mem[in2_addr]
        self.mem[out_addr] = fn(in1, in2)
        return 4  # 1 opcode, 3 params
    def do_opcode_99(self):
        raise Halt()
    def do_opcode_1(self):
        return self.binary_math_op(lambda x, y: x+y)
    def do_opcode_2(self):
        return self.binary_math_op(lambda x, y: x*y)
    def step(self):
        try:
            opcode = self.mem[self.pc]
            do_opcode = getattr(self, f"do_opcode_{opcode}")
        except (IndexError, AttributeError) as err:
            raise SomethingWentWrong() from err
        self.pc += do_opcode()
    def run(self):
        try:
            while True:
                self.step()
        except Halt as err:
            pass
    def __str__(self):
        return ','.join(str(x) for x in self.mem)

class TestProgram(Program):
    def __init__(self, init, in_iter, out_fn):
        super().__init__(init)
        self.in_iter = in_iter  # yields input
        self.out_fn = out_fn  # called with output
    def do_opcode_3(self):
        in_addr = self.param(1)
        in_val = next(self.in_iter)
        self.mem[in_addr] = in_val
        return 2  # 1 opcode, 1 param
    def do_opcode_4(self):
        out_addr = self.param(1)
        out_val = self.mem[out_addr]
        self.out_fn(out_val)
        return 2  # 1 opcode, 1 param
