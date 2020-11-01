#!/usr/bin/env python3
from . import aocutils
from . import aocintcode
from . import aocbreakout


prog = aocutils.input_program("day13_input.txt")
game = aocbreakout.Game(prog, freeplay=True)
game.run()
print(game.score)
