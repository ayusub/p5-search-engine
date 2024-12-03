#!/usr/bin/env python3
"""Final Reducer for Inverted Index."""

import sys
import itertools
import logging

logging.basicConfig(level=logging.DEBUG)

def reduce_one_group(__, group):
    """Reduce one group."""
    term_data = {}
    # duplicates = {}
    # print("group")
    for line in group:
        # print(f"debug: {line}")
        _, term, rest = line.strip().split("\t", 2)
        doc_id, idf, tf, norm = rest.split()

        # Ensure term exists
        if term not in term_data:
            # term_data[term] = []
            output = f"{idf} {doc_id} {tf} {norm}"
            term_data[term] = output
        else:
            output = f" {doc_id} {tf} {norm}"
            term_data[term] += output

    for term, data in term_data.items():
        print(f"{term} {data}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    # for key, group in itertools.groupby(sys.stdin, keyfunc):
    #     # print("key: ")
    #     # print(key)
    #     count = 0;
    #     print("group: ")
    #     print(count)
    #     count += 1
    #     for line in group:
    #         # Strip leading/trailing whitespace from each line
    #         line = line.strip()
    #         # Skip empty lines (if any)
    #         if line:
    #             print(line)
    # sorted_lines = sorted(sys.stdin, key=keyfunc)
    # for key, group in itertools.groupby(sorted_lines, keyfunc):
    #     for line in group:
    #         logging.debug(f"{key}:{line}")

    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
