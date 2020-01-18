import collections


class SpaceObject(object):
    def __init__(self):
        self.orbited_by = []
        self.orbits = None
    def count_orbits(self, omap):
        if self.orbits is None:
            self.orbit_count = 0
        else:
            self.orbit_count = 1 + omap.objects[self.orbits].orbit_count
        return self.orbit_count


class OrbitMap(object):
    def __init__(self):
        self.objects = collections.defaultdict(SpaceObject)
    def input_orbits(self, orbit_iter):
        for orbit_desc in orbit_iter:
            orbited, orbitor = orbit_desc.strip().split(')')
            self.objects[orbited].orbited_by.append(orbitor)
            self.objects[orbitor].orbits = orbited
        # Sorted, breadth first enumeration of objects
        self.object_order = ['COM']
        for o in self.object_order:
            self.object_order.extend(self.objects[o].orbited_by[:])
    def walk(self):
        for oname in self.object_order:
            yield self.objects[oname]
    def count_orbits(self):
        return sum(o.count_orbits(self) for o in self.walk())


def count_orbits(orbit_iter):
    omap = OrbitMap()
    omap.input_orbits(orbit_iter)
    return omap.count_orbits()
