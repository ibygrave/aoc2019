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
