import collections
import sys


class SpaceObject(object):
    def __init__(self):
        self.orbited_by = []
        self.orbits = None

    def count_orbits(self, omap):
        if self.orbits is None:
            self.depth = 0
        else:
            self.depth = 1 + omap[self.orbits].depth
        return self.depth


class OrbitMap(collections.defaultdict):
    def __init__(self):
        super().__init__(SpaceObject)

    def input_orbits(self, orbit_iter):
        for orbit_desc in orbit_iter:
            orbited, orbitor = orbit_desc.strip().split(')')
            self[orbited].orbited_by.append(orbitor)
            self[orbitor].orbits = orbited
        # Sorted, breadth first enumeration of objects
        self.object_order = ['COM']
        for o in self.object_order:
            self.object_order.extend(self[o].orbited_by[:])

    def walk(self):
        for oname in self.object_order:
            yield self[oname]

    def count_orbits(self):
        return sum(o.count_orbits(self) for o in self.walk())

    def plan_route(self, start, end):
        # plan route via nearest common ancestor in tree of orbits
        # route consists of two parts, up the tree to nca,
        # then down the tree to goal
        up = []
        down = []
        min_depth = min(self[start].depth, self[end].depth)
        # get both sides of the route to the same depth
        while self[start].depth > min_depth:
            start = self[start].orbits
            up.append(start)
        while self[end].depth > min_depth:
            end = self[end].orbits
            down.append(end)
        # get both sides of the route to the nca
        while start != end:
            start = self[start].orbits
            up.append(start)
            end = self[end].orbits
            down.append(end)
        down.reverse()
        assert up[-1] == down[0]
        return up + down[1:]


def count_orbits(orbit_iter):
    omap = OrbitMap()
    omap.input_orbits(orbit_iter)
    return omap.count_orbits()


def day6():
    # Part 1
    print("part 1")
    with open(sys.argv[1]) as input_file:
        print(count_orbits(input_file))
    # Part 2
    print("part 2")
    omap = OrbitMap()
    with open(sys.argv[1]) as input_file:
        omap.input_orbits(input_file)
    omap.count_orbits()
    print(len(omap.plan_route("YOU", "SAN"))-1)
