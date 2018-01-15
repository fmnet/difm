#!/bin/sh
INSTALL_PATH=/Users/pgdx-seth/git/difm

PYTHONPATH=$INSTALL_PATH:$PYTHONPATH
cd "$INSTALL_PATH"
pipenv run difm $*
