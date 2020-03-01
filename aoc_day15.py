#!/usr/bin/env python3
import aocutils
import aocintcode
import aocrepairdroid


prog = aocutils.input_program("day15_input.txt")
aocrepairdroid.search(sense_control=prog, stop_at_oxygen=True)
# search again, starting from the oxygen system
aocrepairdroid.search(sense_control=prog, stop_at_oxygen=False)
