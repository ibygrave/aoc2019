#!/bin/bash
set -ex

pytest-3

for q in ./aoc_day*.py; do echo $q; $q; done > answers.txt

echo DONE
