"""Emergency Hull Painting Robot"""
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
import sys
from . import intcode

D = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def move(loc, d):
    x, y = loc
    dx, dy = D[d]
    return (x + dx, y + dy)


class Robot:
    def __init__(self, controller):
        self.loc = (0, 0)
        self.d = 0
        self.painted = {}
        self.controller = controller

    def _step(self):
        self.controller.set_input([self.painted.get(self.loc, 0)])
        self.painted[self.loc] = next(self.controller)
        if next(self.controller):
            # right
            self.d += 1
        else:
            # left
            self.d -= 1
        self.d = self.d % 4
        self.loc = move(self.loc, self.d)

    def run(self):
        try:
            while True:
                self._step()
        except StopIteration:
            pass

    def _ch(self, loc):
        if loc in self.painted.keys():
            return ".#"[self.painted[loc]]
        return ' '

    def __str__(self):
        painted_locs = self.painted.keys()
        xs = [loc[0] for loc in painted_locs]
        ys = [loc[1] for loc in painted_locs]
        xmin = min(xs)
        xmax = max(xs)
        ymin = min(ys)
        ymax = max(ys)
        rows = []
        for y in range(ymin, ymax+1):
            rows.append(''.join(self._ch((x, y)) for x in range(xmin, xmax+1)))
        return '\n'.join(rows)

    def count_painted(self):
        return len(self.painted.keys())


def day11():
    # Part 1
    print("part 1")
    prog = intcode.input_program(sys.argv[1])
    ehpr = Robot(prog)
    ehpr.run()
    print(ehpr.count_painted())
    # Part 2
    print("part 2")
    prog = intcode.input_program(sys.argv[1])
    ehpr = Robot(prog)
    ehpr.painted[(0, 0)] = 1
    ehpr.run()
    print(ehpr)
