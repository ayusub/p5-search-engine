#!/usr/bin/env python3
"""Reduce 1."""

import sys

# Simply pass through all key-value pairs
for line in sys.stdin:
    # Strip leading/trailing whitespace and output the line
    print(line.strip())
