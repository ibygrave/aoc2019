"""Repair Droid"""
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
import sys
from . import intcode

COMPASS = "!NSWE"
DIR = [
    (0, 0),   # 0: N/A
    (0, -1),  # 1: N
    (0, 1),   # 2: S
    (-1, 0),   # 3: W
    (1, 0),  # 4: E
    ]
LOC_EMPTY = 0
LOC_WALL = 1
LOC_OXY = 2


class Droid:
    def __init__(self, sense_control):
        self.x = 0
        self.y = 0
        self.found = {(0, 0): LOC_EMPTY}
        self.sense_control = sense_control

    def move(self, next_move, move_status):
        dx, dy = DIR[next_move]
        next_loc = (self.x + dx, self.y + dy)
        if move_status == 0:
            # Wall
            self.found[next_loc] = LOC_WALL
        elif move_status == 1:
            # Moved
            self.found[next_loc] = LOC_EMPTY
            self.x, self.y = next_loc
        elif move_status == 2:
            # Moved and found oxygen system
            self.found[next_loc] = LOC_OXY
            self.x, self.y = next_loc

    def __str__(self):
        xmin = min(loc[0] for loc in self.found)
        xmax = max(loc[0] for loc in self.found)
        xspan = 1 + xmax - xmin
        ymin = min(loc[1] for loc in self.found)
        ymax = max(loc[1] for loc in self.found)
        yspan = 1 + ymax - ymin
        rows = [[' ' for _ in range(xspan)] for _ in range(yspan)]
        for x, y in self.found:
            rows[y - ymin][x - xmin] = ".#O"[self.found[(x, y)]]
        rows[self.y - ymin][self.x - xmin] = 'd'
        return '\n'.join(''.join(row) for row in rows) + '\n---\n'


DEADEND = object()  # sentinel


class SearchTree:
    # pylint: disable=too-few-public-methods
    __slots__ = ['x', 'y', 'dirs', 'back', 'depth']

    def __init__(self, loc, back):
        self.x, self.y = loc
        self.dirs = [None, None, None, None]
        self.back = back
        if back is None:
            self.depth = 0
        else:
            self.depth = 1 + back.depth

    def next_move(self, found):
        for move in range(len(self.dirs)):
            if self.dirs[move] is None:
                dx, dy = DIR[move + 1]
                move_loc = (self.x + dx, self.y + dy)
                if move_loc in found:
                    self.dirs[move] = DEADEND
                else:
                    self.dirs[move] = SearchTree(move_loc, self)
                    return (move + 1), self.dirs[move]
        if self.back is None:
            raise StopIteration
        for move, dloc in enumerate(DIR):
            dx, dy = dloc
            if (self.back.x == (self.x + dx)) \
               and (self.back.y == (self.y + dy)):
                return move, self.back
        raise AssertionError("couldn't go back")


def search(sense_control, stop_at_oxygen):
    droid = Droid(sense_control)
    start = SearchTree((droid.x, droid.y), back=None)
    here = start
    maxdepth = 0
    try:
        while True:
            # pick a move to try
            next_move, next_here = here.next_move(droid.found)
            # use sensor program to try move
            sense_control.set_input([next_move])
            move_status = next(sense_control)
            # update repair droid with movement
            droid.move(next_move, move_status)
            # update search tree
            if move_status != 0:
                # Not a wall, move to next_here
                here = next_here
                maxdepth = max(maxdepth, here.depth)
            if stop_at_oxygen and move_status == 2:
                print(f"{here.depth} moves to oxygen")
                return
    except StopIteration:
        print(f"furthest: {maxdepth}")


def day15():
    prog = intcode.input_program(sys.argv[1])
    search(sense_control=prog, stop_at_oxygen=True)
    # search again, starting from the oxygen system
    search(sense_control=prog, stop_at_oxygen=False)
