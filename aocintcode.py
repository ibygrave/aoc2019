from collections import namedtuple
import itertools


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
    def do_opcode_03(self):
        in_val = next(self.in_iter)
        self.put_param(1, in_val)
        self.next_pc = self.pc + 2  # 1 opcode, 1 param
    def do_opcode_04(self):
        self.next_out = self.get_param(1)
        self.next_pc = self.pc + 2  # 1 opcode, 1 param
    def do_opcode_05(self):
        """jump-if-true"""
        if self.get_param(1) != 0:
            self.next_pc = self.get_param(2)
        else:
            self.next_pc = self.pc + 3  # 1 opcode, 2 params
    def do_opcode_06(self):
        """jump-if-false"""
        if self.get_param(1) == 0:
            self.next_pc = self.get_param(2)
        else:
            self.next_pc = self.pc + 3  # 1 opcode, 2 params
    def do_opcode_07(self):
        """less than"""
        if self.get_param(1) < self.get_param(2):
            self.put_param(3, 1)
        else:
            self.put_param(3, 0)
        self.next_pc = self.pc + 4  # 1 opcode, 3 params
    def do_opcode_08(self):
        """equals"""
        if self.get_param(1) == self.get_param(2):
            self.put_param(3, 1)
        else:
            self.put_param(3, 0)
        self.next_pc = self.pc + 4  # 1 opcode, 3 params
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
    def __str__(self):
        return ','.join(str(x) for x in self.mem)
    def set_input(self, in_iter):
        self.in_iter = in_iter  # yields input
    def __iter__(self):
        return self
    def __next__(self):
        self.next_out = None
        while self.running and self.next_out is None:
            self.step()
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


def control_amps(prog, phases, signal=0):
    for phase in phases:
        controller = Program(prog)
        controller.set_input(iter([phase, signal]))
        outputs = list(controller)
        assert len(outputs) == 1
        signal = outputs[0]
    return signal


AmpControl = namedtuple('AmpControl', ['signal', 'phases'])
def optimize_amps(prog, phases):
    best = None
    for phases_perm in itertools.permutations(phases):
        signal = control_amps(prog, phases_perm)
        if best is None or signal > best.signal:
            best = AmpControl(signal, list(phases_perm))
    return best
