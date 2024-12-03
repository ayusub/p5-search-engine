#!/usr/bin/env python3
"""Reduce 3: Calculate Everything Else."""
import sys
import math
import itertools

values = {}


def reduce_one_group(__, group):
    """Reduce one group."""
    with open("total_document_count.txt", 'r', encoding="utf-8") as f:
        collection_size = int(f.read().strip())

    # print(f"key: {key}")
    # doc_list = []  # Temporary list to hold document data for the term
    group_list = list(group)
    nk = len(group_list)
    idf_k = math.log10(float(collection_size)/float(nk))

    # Process each line in the group
    for line in group_list:
        # print("hi")
        if not line.strip():  # Skip empty lines
            continue
        # print("line: ")
        # print(line)
        term, rest = line.split("\t")  # Split term and the rest
        doc_id, tf_ik = rest.split()  # Split rest into doc_id and tf_ik

        print(f"{doc_id}\t{term} {idf_k} {tf_ik}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
