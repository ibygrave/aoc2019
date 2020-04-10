#!/usr/bin/env python3
import aocfft


with open("day16_input.txt") as input_file:
    signal = input_file.read().strip()
print(aocfft.fft(signal, 100)[:8])
