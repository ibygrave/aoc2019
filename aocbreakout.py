from collections import namedtuple

Tile = namedtuple('Tile', ['x', 'y', 'id'])
Bat = namedtuple('Bat', ['x', 'y'])
Ball = namedtuple('Ball', ['x', 'y'])


class Game:
    def __init__(self, prog, freeplay=False, show=False):
        self.prog = prog
        self.xmax, self.ymax = 0, 0
        self.field = None
        self.bat = None
        self.ball = None
        self.score = 0
        self.undrawn = []
        self.show = show
        if freeplay:
            self.prog.mem[0] = 2
        self.prog.set_input_fn(self.joystick)

    def init_field(self):
        self.xmax = 1 + max(b.x for b in self.undrawn)
        self.ymax = 1 + max(b.y for b in self.undrawn)
        self.field = [([0] * self.xmax) for _ in range(self.ymax)]

    def draw(self):
        if self.field is None:
            self.init_field()
        for block in self.undrawn:
            if block.x == -1 and block.y == 0:
                self.score = block.id
            elif block.id == 3:
                self.bat = Bat(block.x, block.y)
            elif block.id == 4:
                self.ball = Ball(block.x, block.y)
            else:
                self.field[block.y][block.x] = block.id
        self.undrawn = []
        if self.show:
            print(self)

    def joystick(self):
        self.draw()
        return int(self.bat.x < self.ball.x) - int(self.bat.x > self.ball.x)

    def run(self):
        while True:
            try:
                self.undrawn.append(
                    Tile(next(self.prog),
                         next(self.prog),
                         next(self.prog)))
            except StopIteration:
                self.draw()
                return

    def blockat(self, x, y):
        if self.bat.x == x and self.bat.y == y:
            return '-'
        if self.ball.x == x and self.ball.y == y:
            return 'o'
        return ' #H'[self.field[y][x]]

    def __str__(self):
        return '\n'.join(
            ''.join(
                self.blockat(x, y)
                for x in range(self.xmax))
            for y in range(self.ymax)) \
                                + '\nSCORE: {}'.format(self.score)

    def count_blocks(self, block_id):
        assert block_id < 3
        count = 0
        for x in range(self.xmax):
            for y in range(self.ymax):
                if self.field[y][x] == block_id:
                    count += 1
        return count
