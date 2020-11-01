#!/bin/bash
set -e
tox | tee data/answers.txt.new
mv data/answers.txt.new data/answers.txt
echo DONE
