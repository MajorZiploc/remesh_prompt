#!/bin/sh

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

manage="$SCRIPTPATH/../manage.py" 

python "$manage" test body_comp

