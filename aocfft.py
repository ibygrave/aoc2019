from itertools import islice
import numpy
import numpy.linalg


def pattern(rep):
    while True:
        for mul in [0, 1, 0, -1]:
            for _ in range(rep):
                yield mul


def phase_matrix(size):
    return numpy.array([
        list(islice(pattern(1 + row_ix), 1, size+1))
        for row_ix in range(size)])


def fft(signal, phases):
    signal = [int(digit) for digit in signal]
    one_phase = phase_matrix(len(signal))
    for _ in range(phases):
        signal = numpy.dot(one_phase, signal)
        signal = [abs(digit) % 10 for digit in signal]
    return ''.join(map(str, signal))
