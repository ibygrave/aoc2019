#!/usr/bin/python3
from . import aocfuel
from . import aocutils

print(aocfuel.total_fuel_by_module_mass(aocutils.input_ints("day1_input.txt")))
