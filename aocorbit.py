import collections

def sort_orbits(orbit_iter):
    orbits = collections.defaultdict(list)
    for orbit_desc in orbit_iter:
        orbited, orbitor = orbit_desc.strip().split(')')
        orbits[orbited].append(orbitor)
    planets = ['COM']  # sorted, breadth first enumeration of orbits
    for planet in planets:
        for orbitor in orbits[planet]:
            yield (planet, orbitor)
        planets.extend(orbits[planet][:])


def count_orbits(orbit_iter):
    total_orbits = 0
    planet_orbits = {'COM': 0}
    for orbited, orbitor in sort_orbits(orbit_iter):
        new_orbits = 1 + planet_orbits[orbited]
        planet_orbits[orbitor] = new_orbits
        total_orbits += new_orbits
    return total_orbits
