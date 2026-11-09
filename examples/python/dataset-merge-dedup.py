#!/usr/bin/env python3
"""Run innovative_cookie/dataset-merge-dedup.

Store: https://apify.com/innovative_cookie/dataset-merge-dedup
See run_actor.py for options.
"""
import runpy
import sys
from pathlib import Path

sys.argv = [sys.argv[0], "dataset-merge-dedup", *sys.argv[1:]]
runpy.run_path(str(Path(__file__).with_name("run_actor.py")), run_name="__main__")
