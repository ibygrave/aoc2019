import os
import subprocess
import pytest

DATA_DIR=os.path.dirname(__file__)
ALL_DAYS=list(range(1, 17))


def input_file(day):
    return os.path.join(DATA_DIR, f'day{day}_input.txt')


def output_file(day):
    return os.path.join(DATA_DIR, f'day{day}_output.txt')


@pytest.mark.parametrize("day", ALL_DAYS)
def test_regression_puzzles(day):
    if not os.path.exists(output_file(day)):
        pytest.skip("no expected output data file")

    with open(output_file(day), 'r') as f:
        expected_output_data = f.read()

    output_data = subprocess.check_output([f'aoc_day{day}', input_file(day)]).decode('utf-8')
    assert output_data == expected_output_data


@pytest.mark.parametrize("day", ALL_DAYS)
def test_generate_puzzles(day):
    if os.path.exists(output_file(day)):
        pytest.skip("output data file already exists")

    output_data = subprocess.check_output([f'aoc_day{day}', input_file(day)]).decode('utf-8')
    with open(output_file(day), 'w') as f:
        f.write(output_data)
