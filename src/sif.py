import sys
import numpy


class Image(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layers = []

    def input(self, data):
        digits = (int(digit) for digit in data)
        layer = []
        for digit in digits:
            layer.append(digit)
            if len(layer) == self.width * self.height:
                self.layers.append(layer)
                layer = []
        assert not layer

    def digit_counts(self):
        ret = []
        for layer in self.layers:
            a = numpy.array(layer)
            unique, counts = numpy.unique(a, return_counts=True)
            ret.append(dict(zip(unique, counts)))
        return ret

    def elf_check(self):
        dc = self.digit_counts()
        dc.sort(key=lambda ldc: ldc.get(0, 0))
        return dc[0].get(1, 0) * dc[0].get(2, 0)

    def __str__(self):
        res = ''
        for y in range(self.height):
            for x in range(self.width):
                res += {0: '0', 1: '1'}[self.colour(x, y)]
            res += '\n'
        return res

    def colour(self, x, y):
        layer_ix = (self.width * y) + x
        for layer in self.layers:
            if layer[layer_ix] == 2:
                continue
            return layer[layer_ix]


def day8():
    # Part 1
    print("part 1")
    i = Image(25, 6)
    with open(sys.argv[1]) as input_file:
        i.input(input_file.readline().strip())
    print(i.elf_check())
    # Part 2
    print("part 2")
    print(i)
