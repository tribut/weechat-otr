#!/bin/sh

pylint --rcfile=pylint.rc weechat_otr.py
pylint --rcfile=pylint.rc weechat_otr_test

UNITTEST_COMMAND="python -m unittest"

# Python 2.6 compatibility
python -m unittest -f >/dev/null 2>&1 || UNITTEST_COMMAND="unit2"

$UNITTEST_COMMAND discover
