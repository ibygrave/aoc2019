import pytest
from aoc2019 import asteroids


@pytest.mark.parametrize("mapstr", [
    ".",
    "#",
    """.#..#
.....
#####
....#
...##""",
    ])
def test_io(mapstr):
    am = asteroids.AsteroidMap(mapstr.split('\n'))
    assert str(am) == mapstr


@pytest.mark.parametrize("mapstr, x, y, detects", [
    (""".#..#
.....
#####
....#
...##""", 3, 4, 8),
    ("""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""", 5, 8, 33),
    ("""#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""", 1, 2, 35),
    (""".#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""", 6, 3, 41),
    (""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""", 11, 13, 210),
    ])
def test_best_monitor(mapstr, x, y, detects):
    am = asteroids.AsteroidMap(mapstr.split('\n'))
    best = am.best_monitor()
    assert best.detects == detects
    assert best.x == x
    assert best.y == y


@pytest.mark.parametrize("mapstr, ims_x, ims_y, vaporized", [
    (""".#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##""", 8, 3, [
        (1, 8, 1), (2, 9, 0), (3, 9, 1), (4, 10, 0), (5, 9, 2),
        (6, 11, 1), (7, 12, 1), (8, 11, 2), (9, 15, 1),
        (10, 12, 2), (11, 13, 2), (12, 14, 2), (13, 15, 2), (14, 12, 3),
        (15, 16, 4), (16, 15, 4), (17, 10, 4), (18, 4, 4),
        (19, 2, 4), (20, 2, 3), (21, 0, 2), (22, 1, 2), (23, 0, 1),
        (24, 1, 1), (25, 5, 2), (26, 1, 0), (27, 5, 1),
        (28, 6, 1), (29, 6, 0), (30, 7, 0), (31, 8, 0), (32, 10, 1),
        (33, 14, 0), (34, 16, 1), (35, 13, 3), (36, 14, 3),
    ]),
    (""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""", 11, 13, [
        (1, 11, 12), (2, 12, 1), (3, 12, 2),
        (10, 12, 8), (20, 16, 0), (50, 16, 9),
        (100, 10, 16), (199, 9, 6), (200, 8, 2),
        (201, 10, 9), (299, 11, 1),
    ])
])
def test_vaporize(mapstr, ims_x, ims_y, vaporized):
    am = asteroids.AsteroidMap(mapstr.split('\n'))
    got_vaporized = list(am.vaporize(ims_x, ims_y))
    for v_ix, ax, ay in vaporized:
        assert v_ix <= len(got_vaporized)
        assert ax == got_vaporized[v_ix - 1].x
        assert ay == got_vaporized[v_ix - 1].y