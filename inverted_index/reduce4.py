#!/usr/bin/env python3
"""Reduce 3: Calculate Everything Else."""
import sys
import math
import itertools

# add dict to make faster
# if else statement, key for dict is doc_id


def reduce_one_group(__, group):
    """Reduce one group."""
    normalization_factor = 0

    group = list(group)

    for line in group:
        line = line.strip()
        doc_id, rest = line.split("\t")
        term, idf_k, tf_ik = rest.split()
        tf_idf = float(tf_ik) * float(idf_k)
        normalization_factor += math.pow(float(tf_idf), 2)

    for line in group:
        line = line.strip()
        doc_id, rest = line.split("\t")
        term, tf_idf, tf_ik = rest.split()
        print(f"{term}\t{doc_id} {tf_idf} {tf_ik} {normalization_factor}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    # for key, group in itertools.groupby(sys.stdin, keyfunc):
    #    for line in group:
    #         # Strip leading/trailing whitespace from each line
    #         line = line.strip()
    #         # Skip empty lines (if any)
    #         if line:
    #             print(line)
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
