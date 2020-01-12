from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'steps'])

class Horiz(namedtuple('Horiz', ['y', 'xmin', 'xmax', 'lsteps', 'rsteps'])):
    __slots__ = ()
    def intersect(self, v):
        if (self.xmin <= v.x <= self.xmax) and (v.ymin <= self.y <= v.ymax):
            if self.rsteps > self.lsteps:
                my_steps = self.lsteps + (v.x - self.xmin)
            else:
                my_steps = self.rsteps + (self.xmax - v.x)
            if v.tsteps > v.bsteps:
                v_steps = v.bsteps + (self.y - v.ymin)
            else:
                v_steps = v.tsteps + (v.ymax - self.y)
            return Point(self.y, v.x, my_steps + v_steps)

class Vert(namedtuple('Vert', ['x', 'ymin', 'ymax', 'bsteps', 'tsteps'])):
    __slots__ = ()
    def intersect(self, h):
        return h.intersect(self)


class WireReader(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.steps = 0
        self.wire = []
        self.h = []
        self.v = []
    def go_h(self, h):
        assert isinstance(h, Horiz)
        assert not self.wire or isinstance(self.wire[-1], Vert)
        self.wire.append(h)
        self.h.append(h)
    def go_v(self, v):
        assert isinstance(v, Vert)
        assert not self.wire or isinstance(self.wire[-1], Horiz)
        self.wire.append(v)
        self.v.append(v)
    def go_R(self, l):
        self.go_h(Horiz(self.y, self.x, self.x+l, self.steps, self.steps+l))
        self.x += l
        self.steps += l
    def go_L(self, l):
        self.go_h(Horiz(self.y, self.x-l, self.x, self.steps+l, self.steps))
        self.x -= l
        self.steps += l
    def go_U(self, l):
        self.go_v(Vert(self.x, self.y, self.y+l, self.steps, self.steps+l))
        self.y += l
        self.steps += l
    def go_D(self, l):
        self.go_v(Vert(self.x, self.y-l, self.y, self.steps+l, self.steps))
        self.y -= l
        self.steps += l
    def read(self, text):
        for seg in text.strip().split(','):
            d, l = seg[0], int(seg[1:])
            getattr(self, f"go_{d}")(l)


def cross_intersect(mine, yours):
    for my_s in mine:
        for your_s in yours:
            i = my_s.intersect(your_s)
            if i is not None:
                yield i

class Wire(object):
    def __init__(self, text):
        r = WireReader()
        r.read(text)
        self.h = r.h
        self.v = r.v
    def intersections(self, other):
        yield from cross_intersect(self.h, other.v)
        yield from cross_intersect(self.v, other.h)
    def distance_closest_cross(self, other):
        closest_d = None
        for p in self.intersections(other):
            d = abs(p.x) + abs(p.y)
            if d == 0:
                continue
            if closest_d is None or d < closest_d:
                closest_d = d
        return closest_d
    def steps_first_cross(self, other):
        first_s = None
        for p in self.intersections(other):
            if p.steps == 0:
                continue
            if first_s is None or p.steps < first_s:
                first_s = p.steps
        return first_s
