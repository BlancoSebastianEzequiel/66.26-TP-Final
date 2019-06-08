#!/usr/bin/env bash

echo "DELETING ALL __PYCACHE__ DIRECTORIES"
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf