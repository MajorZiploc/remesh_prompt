#!/bin/sh

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

"$SCRIPTPATH/make_migrates.sh"
"$SCRIPTPATH/migrate.sh"

