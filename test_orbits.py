import pytest
import aocorbit

@pytest.mark.parametrize("orbit_map, orbit_count", [
    ("COM)B,B)C,C)D,D)E,E)F,B)G,G)H,D)I,E)J,J)K,K)L", 42),
    ])
def test_count_orbits(orbit_map, orbit_count):
    assert orbit_count == aocorbit.count_orbits(iter(orbit_map.split(',')))
