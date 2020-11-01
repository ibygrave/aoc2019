from math import gcd
import re
from .aocutils import pairs, sign


MOON_RE = re.compile(r'<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>')


class Coord:
    __slots__ = ['c', 'dc']

    def __init__(self, c):
        self.c = c
        self.dc = 0

    def apply_gravity(self, other):
        ddc = sign(other.c - self.c)
        self.dc += ddc
        other.dc -= ddc

    def apply_velocity(self):
        self.c += self.dc


CNAMES = ['x', 'y', 'z']


class MoonSim:
    def __init__(self, scanlines):
        self.coords = {}
        for cname in CNAMES:
            self.coords[cname] = []
        for scanline in scanlines:
            coords = MOON_RE.match(scanline).groupdict()
            for cname in CNAMES:
                self.coords[cname].append(Coord(int(coords[cname])))

    def apply_gravity(self, coords=CNAMES):
        for cname in coords:
            for c1, c2 in pairs(self.coords[cname]):
                c1.apply_gravity(c2)

    def apply_velocity(self, coords=CNAMES):
        for cname in coords:
            for c1 in self.coords[cname]:
                c1.apply_velocity()

    def step(self, nsteps=1, coords=CNAMES):
        for _ in range(nsteps):
            self.apply_gravity(coords)
            self.apply_velocity(coords)

    def get_state(self, coords=CNAMES):
        return [tuple([c.c for c in cs] + [c.dc for c in cs])
                for cs in zip(*[self.coords[cname]
                                for cname in coords])]

    def total_energy(self):
        energy = 0
        for moon_coords in zip(*self.coords.values()):
            potential = 0
            kinetic = 0
            for moon_coord in moon_coords:
                potential += abs(moon_coord.c)
                kinetic += abs(moon_coord.dc)
            energy += potential * kinetic
        return energy

    def repeat_period(self):
        # As gravity and velocity operations are reversible,
        # only need to check for return to state at time 0.
        # If state could repeat without passing through state
        # at time 0 then universe could run backwards to a
        # different state, so would not be reversible.
        # As evolution of x-coordinates are independant of
        # evolution of other coordinates, then can find
        # repeat period of each coordinate seperately and
        # then combine.
        period = 1
        for cname in CNAMES:
            c0 = self.get_state([cname])
            self.step(coords=[cname])
            nsteps = 1
            while self.get_state([cname]) != c0:
                self.step(coords=[cname])
                nsteps += 1
            period *= nsteps // gcd(nsteps, period)
        return period
