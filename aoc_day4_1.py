#!/usr/bin/python3
import aocpasswordguesser


def count_valid_passwords(first, last):
    d = aocpasswordguesser.to_digits(first)
    count = 0
    while aocpasswordguesser.from_digits(d) <= last:
        if aocpasswordguesser.has_double(d):
            count += 1
        aocpasswordguesser.incr_nondecr(d)
    return count


if __name__ == '__main__':
    # Input: 240920-789857
    print(count_valid_passwords(244444, 789857))
