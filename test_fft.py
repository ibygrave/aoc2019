import pytest
import aocfft

@pytest.mark.parametrize("signal, phases, output", [
    ("12345678", 1, "48226158"),
    ("12345678", 2, "34040438"),
    ("12345678", 3, "03415518"),
    ("12345678", 4, "01029498"),
    ("80871224585914546619083218645595", 100, "24176176"),
    ("19617804207202209144916044189917", 100, "73745418"),
    ("69317163492948606335995924319873", 100, "52432133"),
    ])
def test_fft(signal, phases, output):
    assert aocfft.fft(signal, phases).startswith(output)
