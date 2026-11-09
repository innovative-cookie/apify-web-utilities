#!/usr/bin/env python3
"""Run innovative_cookie/broken-link-checker. See run_actor.py for options."""
import runpy
import sys
from pathlib import Path

sys.argv = [sys.argv[0], "broken-link-checker", *sys.argv[1:]]
runpy.run_path(str(Path(__file__).with_name("run_actor.py")), run_name="__main__")
