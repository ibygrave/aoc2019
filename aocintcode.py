class SomethingWentWrong(Exception):
    pass


class Program(object):
    def __init__(self, init, clone=None):
        if clone is not None:
            self.mem = clone.mem[:]
        else:
            self.mem = list(map(int, init.strip().split(',')))
        self.pc = 0
        self.running = True
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
        self.next_pc = self.pc + 4  # 1 opcode, 3 params
    def do_opcode_99(self):
        self.running = False
    def do_opcode_01(self):
        self.binary_math_op(lambda x, y: x+y)
    def do_opcode_02(self):
        self.binary_math_op(lambda x, y: x*y)
    def step(self):
        self.next_pc = None
        try:
            instr = self.mem[self.pc]
            instr = f"{instr:02}"
            opcode = instr[-2:]
            self.param_modes = list(int(m) for m in instr[:-2])[::-1]
            do_opcode = getattr(self, f"do_opcode_{opcode}")
        except (IndexError, AttributeError) as err:
            raise SomethingWentWrong() from err
        do_opcode()
        self.pc = self.next_pc
    def run(self):
        while self.running:
            self.step()
    def __str__(self):
        return ','.join(str(x) for x in self.mem)

class TestProgram(Program):
    def set_input(self, in_iter):
        self.in_iter = in_iter  # yields input
    def do_opcode_03(self):
        in_val = next(self.in_iter)
        self.put_param(1, in_val)
        self.next_pc = self.pc + 2  # 1 opcode, 1 param
    def do_opcode_04(self):
        self.next_out = self.get_param(1)
        self.next_pc = self.pc + 2  # 1 opcode, 1 param
    def __iter__(self):
        return self
    def __next__(self):
        self.next_out = None
        while self.running and self.next_out is None:
            super().step()
        if self.next_out is None:
            raise StopIteration()
        else:
            return self.next_out


def run_test_program(prog, system_ids=[1]):
    prog.set_input(iter(system_ids))
    outputs = list(prog)
    errors, diagnostic = outputs[:-1], outputs[-1]
    assert all(error == 0 for error in errors)
    return diagnostic
