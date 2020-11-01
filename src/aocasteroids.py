from collections import defaultdict
from math import atan2, gcd
from .aocutils import pairs


class Asteroid:
    __slots__ = ['x', 'y', 'detects', 'r']

    def __init__(self, x, y):
        self.x = x
        self.y = y
        # How many other asteroids detectable from here
        self.detects = 0
        # Polar-ish coordinates from chosen IMS
        # delta x = dx * r
        # delta y = dy * r
        # dx and dy have no common factors

    def polar_from_ims(self, ims_x, ims_y):
        dx = self.x - ims_x
        dy = self.y - ims_y
        assert (dx != 0) or (dy != 0)
        self.r = gcd(dx, dy)
        dx = dx // self.r
        dy = dy // self.r
        return (dx, dy)


class AsteroidMap(object):
    def __init__(self, mapstr):
        self.asteroids = []
        self.grid = []
        for y, rowstr in enumerate(mapstr):
            row = []
            for x, cellstr in enumerate(rowstr):
                if cellstr == '#':
                    cell = Asteroid(x, y)
                else:
                    cell = None
                row.append(cell)
                if cell is not None:
                    self.asteroids.append(cell)
            self.grid.append(row)
        self.xmax = len(self.grid[0])
        self.maxy = len(self.grid)

    def __str__(self):
        return '\n'.join(
                ''.join(cell and '#' or '.' for cell in row)
                for row in self.grid)

    def _can_detect(self, a1, a2):
        x, y = a1.x, a1.y
        dx = a2.x - x
        dy = a2.y - y
        g = gcd(dx, dy)
        if g == 1:
            return True
        dx = dx // g
        dy = dy // g
        for s in range(g-1):
            x += dx
            y += dy
            if self.grid[y][x] is not None:
                # obstacle here
                return False
        return True

    def _calc_detects(self):
        for a1, a2 in pairs(self.asteroids):
            if self._can_detect(a1, a2):
                a1.detects += 1
                a2.detects += 1

    def best_monitor(self):
        self._calc_detects()
        self.asteroids.sort(key=lambda a: a.detects, reverse=True)
        return self.asteroids[0]

    def vaporize(self, ims_x, ims_y):
        ims = self.grid[ims_y][ims_x]
        assert ims is not None
        polar = defaultdict(list)  # direction -> list of asteroids
        for a in self.asteroids:
            if a is not ims:
                polar[a.polar_from_ims(ims_x, ims_y)].append(a)
        for line in polar.values():
            line.sort(key=lambda a: a.r)  # nearest first
        directions = list(polar.keys())
        directions.sort(key=lambda d: -atan2(d[0], d[1]))  # clockwise from N
        queues = [polar[d] for d in directions if polar[d]]
        while queues:
            aim = queues.pop(0)
            yield aim.pop(0)
            if aim:
                # More asteroids in that direction
                queues.append(aim)
