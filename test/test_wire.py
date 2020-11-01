import pytest
from aoc2019 import wire


@pytest.mark.parametrize("wire1,wire2,closest_cross", [
    (
        "R8,U5,L5,D3",
        "U7,R6,D4,L4",
        6
    ),
    (
        "R75,D30,R83,U83,L12,D49,R71,U7,L72",
        "U62,R66,U55,R34,D71,R55,D58,R83",
        159
    ),
    (
        "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
        "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        135
    ),
    ])
def test_closest_cross(wire1, wire2, closest_cross):
    w1 = wire.Wire(wire1)
    w2 = wire.Wire(wire2)
    assert closest_cross == w1.distance_closest_cross(w2)
    assert closest_cross == w2.distance_closest_cross(w1)


@pytest.mark.parametrize("wire1,wire2,first_cross", [
    (
        "R8,U5,L5,D3",
        "U7,R6,D4,L4",
        30
    ),
    (
        "R75,D30,R83,U83,L12,D49,R71,U7,L72",
        "U62,R66,U55,R34,D71,R55,D58,R83",
        610
    ),
    (
        "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
        "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        410
    ),
    ])
def test_first_cross(wire1, wire2, first_cross):
    w1 = wire.Wire(wire1)
    w2 = wire.Wire(wire2)
    assert first_cross == w1.steps_first_cross(w2)
    assert first_cross == w2.steps_first_cross(w1)
