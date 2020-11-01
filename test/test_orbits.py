import pytest
from aoc2019 import orbit


@pytest.mark.parametrize("orbit_map, orbit_count", [
    ("COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L", 42),
    ])
def test_count_orbits(orbit_map, orbit_count):
    assert orbit_count == orbit.count_orbits(iter(orbit_map.split(',')))


@pytest.mark.parametrize("orbit_map, route", [
    (
        "COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L,K)YOU,I)SAN",
        ["K", "J", "E", "D", "I"],
        ),
    (
        "COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L,I)YOU,I)SAN",
        ["I"],
        ),
    ])
def test_plan_route(orbit_map, route):
    omap = orbit.OrbitMap()
    omap.input_orbits(iter(orbit_map.split(',')))
    omap.count_orbits()
    planned_route = omap.plan_route("YOU", "SAN")
    assert route == planned_route
