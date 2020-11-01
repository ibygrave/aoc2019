#!/usr/bin/env python3
from . import aocutils
from . import aocintcode
from . import aocrepairdroid


prog = aocutils.input_program("day15_input.txt")
aocrepairdroid.search(sense_control=prog, stop_at_oxygen=True)
# search again, starting from the oxygen system
aocrepairdroid.search(sense_control=prog, stop_at_oxygen=False)
