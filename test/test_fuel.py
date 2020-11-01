import pytest
from aoc2019 import fuel


@pytest.mark.parametrize("module_mass, need_fuel", [
    (12, 2), (14, 2), (1969, 654), (100756, 33583), (2, 0)])
def test_fuel_from_module_mass(module_mass, need_fuel):
    assert need_fuel == fuel.fuel_by_module_mass(module_mass)


@pytest.mark.parametrize("module_mass, need_fuel", [
    (14, 2), (1969, 966), (100756, 50346)])
def test_rocket_fuel(module_mass, need_fuel):
    assert need_fuel == fuel.rocket_fuel(module_mass)
