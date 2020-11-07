import sys

DLEN = 6


def to_digits(n, dlen=DLEN):
    d = list(int(i) for i in str(n))
    assert len(d) == dlen
    return d


def from_digits(d):
    if not d:
        return 0
    return 10 * from_digits(d[:-1]) + d[-1]


def incr_nondecr(d, dlen=DLEN):
    for non_max_ix in range(dlen-1, -1, -1):
        if d[non_max_ix] < 9:
            break
    else:
        raise ValueError("Overflow")
    d[non_max_ix] += 1
    min_d = d[non_max_ix]
    for ix in range(non_max_ix+1, dlen):
        d[ix] = min_d


def has_double(d):
    return any(fst == nxt for fst, nxt in zip(d[:-1], d[1:]))


def has_lonely_double(d):
    m = list(d[ix] == d[ix+1] for ix in range(5))
    if m[0] and not m[1]:
        return True
    if m[1] and not (m[0] or m[2]):
        return True
    if m[2] and not (m[1] or m[3]):
        return True
    if m[3] and not (m[2] or m[4]):
        return True
    if m[4] and not m[3]:
        return True
    return False


def count_valid_passwords(first, last, p_valid):
    d = to_digits(first)
    count = 0
    while from_digits(d) <= last:
        if p_valid(d):
            count += 1
        incr_nondecr(d)
    return count


def day4():
    # Input: 240920-789857
    # Part 1
    print("part 1")
    print(count_valid_passwords(244444, 789857, has_double))
    # Part 2
    print("part 2")
    print(count_valid_passwords(244444, 789857, has_lonely_double))
