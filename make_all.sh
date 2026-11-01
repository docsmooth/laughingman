#! /bin/bash
# Builds every watch style.  Requires Python 3 with Pillow (PIL);
# set PYTHON to a specific interpreter if python3 does not have it.
PYTHON=${PYTHON:-python3}
NAME=laughingman

$PYTHON config_watch.py -sa -S -w || exit
pebble build || exit
mv build/$NAME.pbw build/rosewright_a.pbw

$PYTHON config_watch.py -sb -S -w || exit
pebble build || exit
mv build/$NAME.pbw build/rosewright_b.pbw

$PYTHON config_watch.py -sc -c -w -x || exit
pebble build || exit
mv build/$NAME.pbw build/rosewright_c2.pbw

$PYTHON config_watch.py -sd -S || exit
pebble build || exit
mv build/$NAME.pbw build/rosewright_d.pbw

$PYTHON config_watch.py -se -S || exit
pebble build || exit
mv build/$NAME.pbw build/rosewright_e.pbw
