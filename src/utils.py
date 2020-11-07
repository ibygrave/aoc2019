def input_ints(input_name):
    with open(input_name) as input_file:
        for input_line in input_file:
            yield int(input_line.strip())


def pairs(items):
    for ix, item1 in enumerate(items):
        for item2 in items[:ix]:
            yield item1, item2


def sign(a):
    return int(a > 0) - int(a < 0)
