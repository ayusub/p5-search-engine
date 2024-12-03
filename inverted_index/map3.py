#!/usr/bin/env -S python3 -u
"""Map 3: Calculate Everything Else."""
import sys

# JOB 3: tf-idf score, doc_id, tf fin doc, ....
# input: term : doc_id frequency

for line in sys.stdin:
    term, rest = line.split("\t")
    doc_id, tf_ik = rest.split()
    print(f"{term}\t{doc_id} {tf_ik}")
