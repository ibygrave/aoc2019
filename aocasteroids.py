from math import gcd


class Asteroid:
    __slots__ = ['x', 'y', 'detects']
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.detects = 0


def pairs(l):
    for ix, i1 in enumerate(l):
        for i2 in l[:ix]:
            yield i1, i2


class AsteroidMap(object):
    def __init__(self, mapstr):
        self.asteroids = []
        self.grid = []
        for y, rowstr in enumerate(mapstr.split('\n')):
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
        return '\n'.join(''.join(cell and '#' or '.' for cell in row) for row in self.grid)

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
        self.asteroids.sort(key = lambda a: a.detects, reverse=True)
        return self.asteroids[0]
