#!/usr/bin/env bash

pip freeze > dump.txt
pip uninstall -r dump.txt -y
rm dump.txt