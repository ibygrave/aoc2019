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
    def plan_route(self, o_from, o_to):
        # plan route via nearest common ancestor in tree of orbits
        # route consists of two parts, up the tree to nca,
        # then down the tree to goal
        route_up = []
        route_down = []
        def go_up(oname, route):
            transfer = self.objects[oname].orbits
            route.append(transfer)
            return transfer
        # treat orbit_count as depth in orbit map tree
        def get_depth(oname):
            return self.objects[oname].orbit_count
        min_depth = min(get_depth(o_from), get_depth(o_to))
        # get both sides of the route to the same depth
        while get_depth(o_from) > min_depth:
            o_from = go_up(o_from, route_up)
        while get_depth(o_to) > min_depth:
            o_to = go_up(o_to, route_down)
        # get both sides of the route to the nca
        while o_from != o_to:
            o_from = go_up(o_from, route_up)
            o_to = go_up(o_to, route_down)
        route_down.reverse()
        assert route_up[-1] == route_down[0]
        return route_up + route_down[1:]


def count_orbits(orbit_iter):
    omap = OrbitMap()
    omap.input_orbits(orbit_iter)
    return omap.count_orbits()
