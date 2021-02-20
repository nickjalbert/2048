#!/usr/bin/env python
"""
Run flake8 linter on AgentOS Python files

To use::

  $ python scripts/lint_code.py
"""

import os
import sys
from subprocess import run
from subprocess import PIPE

from shared import root_dir
from shared import traverse_tracked_files

returncode = 0

IGNORE_FILES = ["squash_lookup_table.py"]


def flake_file(path):
    global returncode
    extension = os.path.splitext(path)[1]
    if extension != ".py":
        return
    if any(ignored in path for ignored in IGNORE_FILES):
        print(f"====== Skipping {path} in IGNORE_FILES ======\n")
        return
    cmd = ["flake8", "--max-line-length", "79", path]
    result = run(cmd, stdout=PIPE)
    returncode = returncode | result.returncode
    out = result.stdout.decode("utf-8")
    if out:
        print(path)
        print(out)
        print()


traverse_tracked_files(root_dir, flake_file)
sys.exit(returncode)
