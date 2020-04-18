from itertools import count, islice
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


def pascal_diagonal(k):
    """
    Generate the k_th diagonal of Pascal's triangle.
    The 0th diagonal is all ones.
    The 1st diagonal are the counting numbers.
    The 2nd diagonal are the triangular numbers.
    The 3rd diagonal are the tetrahedral numbers.
    Writing 'n choose k' as (n k), this is the infinite sequence:
    (k k) (k+1 k) (k+2 k) ...
    Calculate by starting with 1,
    then for the i_th element multiply by (k+i)/i.
    """
    n_choose_k = 1
    for i in count(1):
        yield n_choose_k
        n_choose_k *= (k+i)
        n_choose_k, remainder = divmod(n_choose_k, i)
        assert remainder == 0


def fft_offset(signal, phases=100, signal_reps=10000, message_len=8):
    assert phases > 0
    offset = int(signal[:7])
    # This algorithm only works when the relevant phase pattern is all ones.
    assert (offset * 2) >= (len(signal) * signal_reps)
    div, mod = divmod(offset, len(signal))
    signal_post = f"{signal[mod:]}{signal*(signal_reps-(div+1))}"
    assert len(signal_post) + offset == len(signal) * signal_reps
    # Expensive:
    # assert (signal*signal_reps).endswith(signal_post)
    digits = [int(digit) for digit in signal_post]
    message = [0] * message_len
    for p_ix, p in enumerate(islice(pascal_diagonal(phases-1), len(digits))):
        for m_ix in range(message_len):
            if (m_ix + p_ix) < len(digits):
                message[m_ix] += (p % 10) * digits[m_ix + p_ix]
                message[m_ix] %= 10
    return ''.join(map(str, message))
