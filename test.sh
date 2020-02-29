#!/bin/bash
set -ex

. .testenv/bin/activate
pytest

for q in ./aoc_day*.py; do echo $q; python $q; done > answers.txt.new
mv answers.txt.new answers.txt

echo DONE
