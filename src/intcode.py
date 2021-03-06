"""IntCode Computer"""
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from collections import namedtuple
import itertools
import sys


class SomethingWentWrong(Exception):
    pass


class ElasticList(list):
    def _ensure_size(self, ix):
        if isinstance(ix, slice):
            ix = ix.stop
            if ix is None:
                return
        while len(self) <= ix:
            self.append(0)

    def __getitem__(self, key):
        self._ensure_size(key)
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        self._ensure_size(key)
        super().__setitem__(key, value)


class Program:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=attribute-defined-outside-init
    def __init__(self, init, clone=None):
        if clone is not None:
            self.mem = clone.mem[:]
        else:
            self.mem = ElasticList(map(int, init.strip().split(',')))
        self.pc = 0
        self.rbase = 0
        self.running = True
        self.inputs = []
        self.input_fn = self.get_input

    def get_input(self):
        return self.inputs.pop(0)

    def param_mode(self, param_ix):
        if param_ix > len(self.param_modes):
            return 0
        return self.param_modes[param_ix-1]

    def get_param(self, param_ix):
        mode = self.param_mode(param_ix)
        param = self.mem[self.pc + param_ix]
        if mode == 0:
            # position
            return self.mem[param]
        if mode == 1:
            # immediate
            return param
        if mode == 2:
            # relative
            return self.mem[self.rbase + param]
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
        elif mode == 2:
            # relative
            self.mem[self.rbase + param] = val
        else:
            raise SomethingWentWrong(f"unknown parameter mode {mode}")

    def step(self):
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        next_pc = self.pc
        next_rbase = self.rbase
        instr = self.mem[self.pc]
        modes, opcode = divmod(instr, 100)
        param_modes = []
        while modes:
            modes, mode = divmod(modes, 10)
            param_modes.append(mode)
        self.param_modes = param_modes
        if opcode == 1:
            self.put_param(3, self.get_param(1) + self.get_param(2))
            next_pc += 4  # 1 opcode, 3 params
        elif opcode == 2:
            self.put_param(3, self.get_param(1) * self.get_param(2))
            next_pc += 4  # 1 opcode, 3 params
        elif opcode == 3:
            in_val = self.input_fn()
            self.put_param(1, in_val)
            next_pc += 2  # 1 opcode, 1 param
        elif opcode == 4:
            self.next_out = self.get_param(1)
            next_pc += 2  # 1 opcode, 1 param
        elif opcode == 5:
            if self.get_param(1) != 0:
                next_pc = self.get_param(2)
            else:
                next_pc += 3  # 1 opcode, 2 params
        elif opcode == 6:
            if self.get_param(1) == 0:
                next_pc = self.get_param(2)
            else:
                next_pc += 3  # 1 opcode, 2 params
        elif opcode == 7:
            if self.get_param(1) < self.get_param(2):
                self.put_param(3, 1)
            else:
                self.put_param(3, 0)
            next_pc += 4  # 1 opcode, 3 params
        elif opcode == 8:
            if self.get_param(1) == self.get_param(2):
                self.put_param(3, 1)
            else:
                self.put_param(3, 0)
            next_pc += 4  # 1 opcode, 3 params
        elif opcode == 9:
            # adjusts the relative base
            next_rbase += self.get_param(1)
            next_pc += 2  # 1 opcode, 1 param
        elif opcode == 99:
            self.running = False
        else:
            raise SomethingWentWrong()
        self.pc = next_pc
        self.rbase = next_rbase

    def __str__(self):
        return ','.join(str(x) for x in self.mem)

    def set_input(self, inputs):
        self.inputs.extend(inputs)

    def set_input_fn(self, input_fn):
        self.input_fn = input_fn

    def __iter__(self):
        return self

    def __next__(self):
        self.next_out = None
        while self.running and self.next_out is None:
            self.step()
        if self.next_out is None:
            raise StopIteration()
        return self.next_out


def run_test_program(prog, system_ids=(1,)):
    prog.set_input(system_ids)
    outputs = list(prog)
    errors, diagnostic = outputs[:-1], outputs[-1]
    assert all(error == 0 for error in errors)
    return diagnostic


def control_amps(prog, phases, signal=0):
    for phase in phases:
        controller = Program(prog)
        controller.set_input([phase, signal])
        outputs = list(controller)
        assert len(outputs) == 1
        signal = outputs[0]
    return signal


def feedback_control_amps(prog, phases, signal=0):
    # pylint: disable=used-before-assignment
    ctrls = []
    for phase in phases:
        ctrl = Program(prog)
        ctrl.set_input([phase])
        ctrls.append(ctrl)
    while True:
        for ctrl in ctrls:
            ctrl.set_input([signal])
            signal = next(ctrl, None)
            if signal is None:
                return signal_out
        signal_out = signal


AmpControl = namedtuple('AmpControl', ['signal', 'phases'])


def optimize_amps(prog, phases, control_fn):
    best = None
    for phases_perm in itertools.permutations(phases):
        signal = control_fn(prog, phases_perm)
        if best is None or signal > best.signal:
            best = AmpControl(signal, list(phases_perm))
    return best


def input_program(input_name, prog_type=Program):
    with open(input_name) as input_file:
        return prog_type(input_file.readline())


def search_params(start_prog, want_out):
    for noun in range(100):
        for verb in range(100):
            experiment = Program("", clone=start_prog)
            experiment.mem[1] = noun
            experiment.mem[2] = verb
            try:
                list(experiment)
            except SomethingWentWrong:
                continue
            if experiment.mem[0] == want_out:
                return f"Found noun = {noun}, verb = {verb}"
    return "Not found"


def day2():
    # Part 1
    prog = input_program(sys.argv[1])
    prog.mem[1] = 12
    prog.mem[2] = 2
    list(prog)
    print("part 1")
    print(prog.mem[0])
    # Part 2
    want = 19690720
    start_prog = input_program(sys.argv[1])
    print("part 2")
    print(search_params(start_prog, want))


def day5():
    # Part 1
    print("part 1")
    prog = input_program(sys.argv[1])
    print(run_test_program(prog))
    # Part 2
    print("part 2")
    prog = input_program(sys.argv[1])
    print(run_test_program(prog, system_ids=[5]))


def day7():
    # Part 1
    print("part 1")
    with open(sys.argv[1]) as input_file:
        prog = input_file.readline()
    phases = [0, 1, 2, 3, 4]
    print(optimize_amps(prog, phases, control_amps))
    # Part 2
    print("part 2")
    with open(sys.argv[1]) as input_file:
        prog = input_file.readline()
    phases = [5, 6, 7, 8, 9]
    print(optimize_amps(prog, phases, feedback_control_amps))


def day9():
    # Part 1
    print("part 1")
    prog = input_program(sys.argv[1])
    print(run_test_program(prog))
    # Part 2
    print("part 2")
    prog = input_program(sys.argv[1])
    print(run_test_program(prog, system_ids=[2]))
