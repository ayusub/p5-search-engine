#!/usr/bin/env python3
"""
Job 2 Reducer: Calculate Term Frequencies (TF).
"""
#idk 
import sys
import itertools

def reduce_one_group(key, group):
    """
    Reduce one group: Compute term frequency (TF) for a single (term, doc_id).
    """
    # Sum the counts for this group
    tf = sum(int(line.split("\t")[2]) for line in group)

    # Emit term, doc_id, and TF
    term, doc_id = key.split()
    print(f"{term}\t{doc_id} {tf}")

def keyfunc(line):
    """
    Extract key (term and doc_id) from the mapper output.
    """
    # Combine term and doc_id as the key
    parts = line.strip().split("\t")
    return f"{parts[1]} {parts[0]}"

def main():
    """
    Read sorted mapper output, group by (term, doc_id), and calculate TF.
    """
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)

if __name__ == "__main__":
    main()
