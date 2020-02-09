from math import gcd
import re
from aocutils import pairs, sign


MOON_RE = re.compile("<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>")


class Moon:
    __slots__ = ['x', 'y', 'z', 'dx', 'dy', 'dz']

    def __init__(self, scanline):
        coords = MOON_RE.match(scanline).groupdict()
        self.x = int(coords['x'])
        self.y = int(coords['y'])
        self.z = int(coords['z'])
        self.dx = 0
        self.dy = 0
        self.dz = 0

    def __str__(self):
        pos = "<x={}, y={}, z={}>".format(self.x, self.y, self.z)
        vel = "<dx={}, dy={}, dz={}>".format(self.dx, self.dy, self.dz)
        return "pos={}, vel={}".format(pos, vel)

    def apply_gravity(self, other):
        ddx = sign(other.x - self.x)
        ddy = sign(other.y - self.y)
        ddz = sign(other.z - self.z)
        self.dx += ddx
        self.dy += ddy
        self.dz += ddz
        other.dx -= ddx
        other.dy -= ddy
        other.dz -= ddz

    def apply_velocity(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

    def potential_energy(self):
        return sum(map(abs, [self.x, self.y, self.z]))

    def kinetic_energy(self):
        return sum(map(abs, [self.dx, self.dy, self.dz]))

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()


class MoonSim:
    def __init__(self, scanlines):
        self.moons = list(map(Moon, scanlines))

    def apply_gravity(self):
        for moon1, moon2 in pairs(self.moons):
            moon1.apply_gravity(moon2)

    def apply_velocity(self):
        for moon in self.moons:
            moon.apply_velocity()

    def step(self, nsteps=1):
        for _ in range(nsteps):
            self.apply_gravity()
            self.apply_velocity()

    def total_energy(self):
        return sum(moon.total_energy() for moon in self.moons)

    def _moon_state(self, attrname):
        return [getattr(m, attrname) for m in self.moons]

    def repeat_period(self):
        # As gravity and velocity operations are reversible,
        # only need to check for return to state at time 0.
        # If state could repeat without passing through state
        # at time 0 then universe could run backwards to a
        # different state, so would not be reversible.
        # As evolution of x-coordinates are independant or
        # evolution of other coordinates, then can find
        # repeat period of each coordinate seperately and
        # then combine.
        x0 = self._moon_state('x')
        dx0 = self._moon_state('dx')
        y0 = self._moon_state('y')
        dy0 = self._moon_state('dy')
        z0 = self._moon_state('z')
        dz0 = self._moon_state('dz')
        x_period = None
        y_period = None
        z_period = None
        nsteps = 0
        while not all([x_period, y_period, z_period]):
            self.step()
            nsteps += 1
            if x_period is None:
                if self._moon_state('x') == x0 and self._moon_state('dx') == dx0:
                    x_period = nsteps
            if y_period is None:
                if self._moon_state('y') == y0 and self._moon_state('dy') == dy0:
                    y_period = nsteps
            if z_period is None:
                if self._moon_state('z') == z0 and self._moon_state('dz') == dz0:
                    z_period = nsteps
        total_period = (x_period * y_period) // gcd(x_period, y_period)
        total_period = (total_period * z_period) // gcd(total_period, z_period)
        return total_period
