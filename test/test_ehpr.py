from aoc2019 import aocehpr


class MockController:
    def __init__(self, moves):
        self.moves = moves
        self.inputs = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.moves:
            return self.moves.pop(0)
        else:
            raise StopIteration

    def set_input(self, i):
        self.inputs.extend(i)


def test_paint():
    c = MockController([1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0])
    r = aocehpr.Robot(c)
    r.run()
    assert str(r) == "  #\n..#\n## "
    assert c.inputs == [0, 0, 0, 0, 1, 0, 0, 0]
    assert r.count_painted() == 6
