#!/usr/bin/env python3
"""Run innovative_cookie/sitemap-extractor.

Store: https://apify.com/innovative_cookie/sitemap-extractor
See run_actor.py for options.
Related: https://dev.to/innovative_cookie/how-to-extract-every-url-from-a-websites-sitemaps-and-check-their-status-codes-python-free-462j
"""
import runpy
import sys
from pathlib import Path

sys.argv = [sys.argv[0], "sitemap-extractor", *sys.argv[1:]]
runpy.run_path(str(Path(__file__).with_name("run_actor.py")), run_name="__main__")
