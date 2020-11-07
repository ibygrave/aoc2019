import os
import subprocess
import pytest

DATA_DIR=os.path.dirname(__file__)


@pytest.mark.parametrize("day", range(1, 17))
def test_puzzles(day):
    input_data_file=os.path.join(DATA_DIR, f'day{day}_input.txt')
    output_data_file=os.path.join(DATA_DIR, f'day{day}_output.txt')

    if os.path.exists(output_data_file):
        with open(output_data_file, 'r') as f:
            expected_output_data = f.read()
    else:
        expected_output_data = None

    output_data = subprocess.check_output([f'aoc_day{day}', input_data_file]).decode('utf-8')

    if expected_output_data is None:
        with open(output_data_file, 'w') as f:
            f.write(output_data)
    else:
        assert output_data == expected_output_data
