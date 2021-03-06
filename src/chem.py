"""Space Stoichiometry"""
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
import functools
import re
import sys

CHEM_RE = re.compile(r'\s*(\d+)\s+([A-Z]+)\s*')


def parse_reaction(text):
    res = {}
    for mul, chem_list in zip([-1, 1], text.split('=>')):
        for chem in chem_list.split(','):
            match = CHEM_RE.match(chem)
            if match is None:
                raise ValueError(
                    "Invalid chemical '{}' reaction: {}".format(chem, text))
            amount, chem_name = match.groups()
            amount = int(amount)
            if chem_name in res:
                raise ValueError(
                    "Duplicate chemical in reaction: {}".format(text))
            res[chem_name] = amount * mul
    return res


def reaction_product(reaction):
    for chem_ix, amount in enumerate(reaction):
        if amount > 0:
            return chem_ix
    raise ValueError("Reaction without product")


def set_union(set1, set2):
    return set1.union(set2)


def union_dict_keys(dicts):
    key_sets = (d.keys() for d in dicts)
    return functools.reduce(set_union, key_sets, set())


def div_round_up(dividend, divisor):
    return (dividend + (divisor-1)) // divisor


class Factory:
    def __init__(self, texts):
        reactions = [parse_reaction(text) for text in texts]
        chems = list(union_dict_keys(reactions))
        chems.sort()  # Sort by name, for stable debug
        self.chem_ix = dict((name, ix) for ix, name in enumerate(chems))
        self.chem_amounts = [0 for _ in chems]
        # Convert reactions from chem:amount dictionary format to arrays
        self.reactions = [
            [reaction.get(chem, 0) for chem in chems]
            for reaction in reactions]
        # List what each reaction makes
        self.reaction_product = [reaction_product(r) for r in self.reactions]

    def __getitem__(self, name):
        return self.chem_amounts[self.chem_ix[name]]

    def __setitem__(self, name, amount):
        self.chem_amounts[self.chem_ix[name]] = amount

    def reduce(self):
        # pylint: disable=cell-var-from-loop
        reacting = True
        while reacting:
            reacting = False
            for r_ix, reaction in enumerate(self.reactions):
                p_ix = self.reaction_product[r_ix]
                if self.chem_amounts[p_ix] < 0:
                    mul = div_round_up(
                        -self.chem_amounts[p_ix], reaction[p_ix])
                    reacting = True
                    self.chem_amounts = list(map(
                        lambda x: x[0] + mul*x[1],
                        zip(self.chem_amounts, reaction)))


def fuel_given_ore(factory, ore_budget, first_step=1000):
    # first guess
    factory['FUEL'] = -first_step
    factory.reduce()
    first_fuel_costs = -factory['ORE']
    est_fuel_cost = (first_step * ore_budget) // first_fuel_costs
    one_fuel_costs = first_fuel_costs // first_step
    # make up fuel to estimated max given budget
    factory['FUEL'] -= (est_fuel_cost - first_step)
    factory.reduce()
    fuel_got = est_fuel_cost
    # keep making more fuel until budget reached
    while (-factory['ORE']) < ore_budget:
        more_fuel = max(1, one_fuel_costs // (ore_budget + factory['ORE']))
        factory['FUEL'] -= more_fuel
        factory.reduce()
        fuel_got += more_fuel
    # Last one went over budget
    fuel_got -= more_fuel
    return fuel_got


def day14():
    # Part 1
    print("part 1")
    with open(sys.argv[1]) as input_file:
        factory = Factory(input_file)
    factory['FUEL'] = -1
    factory.reduce()
    print(-factory['ORE'])
    # Part 2
    print("part 2")
    with open(sys.argv[1]) as input_file:
        factory = Factory(input_file)
    print(fuel_given_ore(factory, ore_budget=1000000000000))
