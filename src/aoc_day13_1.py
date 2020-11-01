#!/usr/bin/env python3
from . import aocutils
from . import aocintcode
from . import aocbreakout


prog = aocutils.input_program("day13_input.txt")
game = aocbreakout.Game(prog)
game.run()
print(game.count_blocks(2))
