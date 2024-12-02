#!/usr/bin/env -S python3 -u
"""Map 3: Calculate Everything Else."""
import sys

# JOB 3: tf-idf score, doc_id, tf fin doc, ....
# input: term : doc_id frequency

# terms = {}
# tf_ik = {}
# read input from previous job output directory ?
for line in sys.stdin:
    # term k
    term, rest = line.split("\t")
    doc_id, tf_ik = rest.split()
    # doc id 
    # print something here ? 
    # tf(ik) = k frequency in i
            # num_docs = terms[k] + 1

            # terms[k] += tf_ik, num_docs[k]`
    print(f"{term}\t{doc_id} {tf_ik}")
