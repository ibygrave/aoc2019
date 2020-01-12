DLEN=6

def to_digits(n, dlen=DLEN):
    d = list(int(i) for i in str(n))
    assert len(d) == dlen
    return d

def from_digits(d):
    return 100000 * d[0] + 10000 * d[1] + 1000 * d[2] + 100 * d[3] + 10 * d[4] + d[5]

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
    # unrolled
    return (d[0] == d[1]) or (d[1] == d[2]) or (d[2] == d[3]) or (d[3] == d[4]) or (d[4] == d[5])

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
