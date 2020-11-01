import pytest
from aoc2019 import aocsif


@pytest.mark.parametrize("w, h, image_data, expected_elf_check", [
    (3, 2, "122456789012", 2),
    (2, 2, "00000100120012101112", 3),
    ])
def test_elf_check(w, h, image_data, expected_elf_check):
    i = aocsif.Image(w, h)
    i.input(image_data)
    assert expected_elf_check == i.elf_check()


def test_render():
    i = aocsif.Image(2, 2)
    i.input("0222112222120000")
    assert "01\n10\n" == str(i)
