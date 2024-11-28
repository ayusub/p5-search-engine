#!/usr/bin/env python3
"""Reduce 0."""

import sys

TOTAL_COUNT = 0

for line in sys.stdin:
    line = line.strip()
    key, value = line.split('\t')
    count = int(value)
    TOTAL_COUNT += count

print(TOTAL_COUNT)
