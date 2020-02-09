#!/usr/bin/python3
import aocfuel
import aocutils

masses = aocutils.input_ints("day1_input.txt")
fuel = aocfuel.total_rocket_fuel_by_module_mass(masses)
print(fuel)
