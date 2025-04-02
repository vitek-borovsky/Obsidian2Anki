#!/usr/bin/env sh
cd $(dirname $0)
rm ObsidianToAnki.log
PYTHONPATH=../../ python manual_invoke.py
