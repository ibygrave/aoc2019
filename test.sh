#!/bin/bash
set -ex

. .testenv/bin/activate
pytest

for q in ./aoc_day*.py; do echo $q; python $q; done > answers.txt

echo DONE
