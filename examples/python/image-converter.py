#!/usr/bin/env python3
"""Run innovative_cookie/image-converter. See run_actor.py for options."""
import runpy
import sys
from pathlib import Path

sys.argv = [sys.argv[0], "image-converter", *sys.argv[1:]]
runpy.run_path(str(Path(__file__).with_name("run_actor.py")), run_name="__main__")
