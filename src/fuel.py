"""AOC2019 fuel"""
import sys
from . import utils


def fuel_by_mass(mass):
    return max(0, (mass // 3) - 2)


fuel_by_module_mass = fuel_by_mass


def total_fuel_by_module_mass(masses):
    return sum(fuel_by_module_mass(mass) for mass in masses)


def rocket_fuel(module_mass):
    unfueled_mass = module_mass
    total_fuel = 0
    while unfueled_mass:
        next_fuel = fuel_by_mass(unfueled_mass)
        total_fuel += next_fuel
        unfueled_mass = next_fuel
    return total_fuel


def total_rocket_fuel_by_module_mass(masses):
    return sum(rocket_fuel(mass) for mass in masses)


def day1():
    # Part 1
    masses = utils.input_ints(sys.argv[1])
    fuel = total_fuel_by_module_mass(masses)
    print("part 1")
    print(fuel)
    # Part 2
    masses = utils.input_ints(sys.argv[1])
    fuel = total_rocket_fuel_by_module_mass(masses)
    print("part 2")
    print(fuel)
