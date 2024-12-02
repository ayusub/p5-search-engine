#!/usr/bin/env python3
"""
Final Reducer for Inverted Index.
"""

import sys
import itertools

def reduce_one_group(key, group):

    term_data = {}
 
    for line in group:
        _, term, rest = line.strip().split("\t", 2)
        doc_id, idf, tf, norm = rest.split()

        # Ensure term exists
        if term not in term_data:
            term_data[term] = []

        # Append document-specific details to the term's list
        term_data[term].append((doc_id, tf, norm, idf))

    # Process and output results for each term
    for term in sorted(term_data.keys()):  # Sort terms lexicographically
        doc_list = sorted(term_data[term], key=lambda x: x[0])  # Sort by doc_id

        output = f"{term} {idf}"
        for doc in doc_list:
            output += f" {doc_id} {tf} {norm}"

        print(output.rstrip())


def keyfunc(line):
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
