#!/usr/bin/env python3
"""
Final Reducer for Inverted Index.
"""

import sys

def reduce_one_group(key, group):

    term_data = {}

    for line in group:
        _, rest = line.strip().split("\t", 1)
        doc_id, idf, tf, norm, term = rest.split()

        # Ensure term exists
        if term not in term_data:
            term_data[term] = []

        # Append document-specific details to the term's list
        term_data[term].append((doc_id, int(tf), float(norm), float(idf)))

    # Process and output results for each term
    for term in sorted(term_data.keys()):  # Sort terms lexicographically
        doc_list = sorted(term_data[term], key=lambda x: x[0])  # Sort by doc_id
        idf = doc_list[0][3]  #idk if this is really needed it might be bad

        # Construct the output line
        doc_details = " ".join(
            f"{doc_id} {tf} {norm}" for doc_id, tf, norm, _ in doc_list
        )
        print(f"{term} {idf} {doc_details}")


def keyfunc(line):
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    import itertools

    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
