#!/usr/bin/python3
from . import aocfuel
from . import aocutils

masses = aocutils.input_ints("day1_input.txt")
fuel = aocfuel.total_rocket_fuel_by_module_mass(masses)
print(fuel)
