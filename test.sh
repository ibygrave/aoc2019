#!/bin/bash
set -ex

. .testenv/bin/activate
python setup.py install
pytest test

ans=$(pwd)/data/answers.txt.new
rm -f $ans
pushd data
for day in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
do
    echo day ${day} >> $ans
    python -m aoc2019.aoc_day${day} >> $ans && continue
    for part in 1 2
    do
        echo part ${part} >> $ans
        python -m aoc2019.aoc_day${day}_${part} >> $ans
    done
done
popd
mv $ans data/answers.txt

echo DONE
