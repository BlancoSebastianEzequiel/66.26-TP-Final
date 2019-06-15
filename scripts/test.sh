#!/usr/bin/env bash

echo "UNIT TESTS"
python -m pytest tests/
sh scripts/delete_pycache.sh
