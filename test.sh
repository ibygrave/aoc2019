#!/bin/bash
set -ex

. .testenv/bin/activate
python setup.py install
pytest test

ans=data/answers.txt.new
rm -f $ans
for day in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
do
    echo day ${day} >> $ans
    aoc_day${day} data/day${day}_input.txt >> $ans
done
mv $ans data/answers.txt

echo DONE
