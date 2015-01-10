#!/bin/bash

UNITTEST_COMMAND="unittest"

# Python 2.6 compatibility
python -m unittest -f >/dev/null 2>&1 || UNITTEST_COMMAND="unit2"

COUNT=0

while $UNITTEST_COMMAND discover; do
  echo $((COUNT+=1))
done
