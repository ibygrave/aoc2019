
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
        self.param_modes = []
    def param_mode(self, param_ix):
        if param_ix > len(self.param_modes):
            return 0
        else:
            return self.param_modes[param_ix-1]
    def get_param(self, param_ix):
        mode = self.param_mode(param_ix)
        param = self.mem[self.pc + param_ix]
        if mode == 0:
            # position
            return self.mem[param]
        elif mode == 1:
            # immediate
            return param
        else:
            raise SomethingWentWrong(f"unknown parameter mode {mode}")
    def put_param(self, param_ix, val):
        mode = self.param_mode(param_ix)
        param = self.mem[self.pc + param_ix]
        if mode == 0:
            # position
            self.mem[param] = val
        elif mode == 1:
            # immediate
            raise SomethingWentWrong("Store immediate")
        else:
            raise SomethingWentWrong(f"unknown parameter mode {mode}")
    def binary_math_op(self, fn):
        in1 = self.get_param(1)
        in2 = self.get_param(2)
        self.put_param(3, fn(in1, in2))
        return 4  # 1 opcode, 3 params
    def do_opcode_99(self):
        raise Halt()
    def do_opcode_01(self):
        return self.binary_math_op(lambda x, y: x+y)
    def do_opcode_02(self):
        return self.binary_math_op(lambda x, y: x*y)
    def step(self):
        try:
            instr = self.mem[self.pc]
            instr = f"{instr:02}"
            opcode = instr[-2:]
            self.param_modes = list(int(m) for m in instr[:-2])[::-1]
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
    def do_opcode_03(self):
        in_val = next(self.in_iter)
        self.put_param(1, in_val)
        return 2  # 1 opcode, 1 param
    def do_opcode_04(self):
        out_val = self.get_param(1)
        self.out_fn(out_val)
        return 2  # 1 opcode, 1 param
