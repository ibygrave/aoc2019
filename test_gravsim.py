import pytest
import aocgravsim


SCAN1 = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

STATE1 = [
        (2, 1, -3, -3, -2, 1),
        (1, -8, 0, -1, 1, 3),
        (3, -6, 1, 3, 2, -3),
        (2, 0, 4, 1, -1, -1)]

SCAN2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""

STATE2 = [
        (8, -12, -9, -7, 3, 0),
        (13, 16, -3, 3, -11, -5),
        (-29, -11, -1, -3, 7, 4),
        (16, -13, 23, 7, 1, 1)]


@pytest.mark.parametrize("scan, nsteps, state", [
    (SCAN1, 10, STATE1),
    (SCAN2, 100, STATE2),
    ])
def test_motion(scan, nsteps, state):
    ms = aocgravsim.MoonSim(scan.split('\n'))
    ms.step(nsteps=nsteps)
    assert ms.get_state() == state


@pytest.mark.parametrize("scan, nsteps, energy", [
    (SCAN1, 10, 179),
    (SCAN2, 100, 1940),
    ])
def test_energy(scan, nsteps, energy):
    ms = aocgravsim.MoonSim(scan.split('\n'))
    ms.step(nsteps=nsteps)
    assert ms.total_energy() == energy


@pytest.mark.parametrize("scan, period", [
    (SCAN1, 2772), (SCAN2, 4686774924)])
def test_period(scan, period):
    ms = aocgravsim.MoonSim(scan.split('\n'))
    assert ms.repeat_period() == period
