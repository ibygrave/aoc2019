#!/usr/bin/python3
import aocsif

i = aocsif.Image(25, 6)
with open("day8_input.txt") as input_file:
    i.input(input_file.readline().strip())
print(i.elf_check())
