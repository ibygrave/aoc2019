import pytest
import aocasteroids


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
    am = aocasteroids.AsteroidMap(mapstr)
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
    am = aocasteroids.AsteroidMap(mapstr)
    best = am.best_monitor()
    assert best.detects == detects
    assert best.x == x
    assert best.y == y
