#!/usr/bin/env python3
"""Job 2 Reducer: Calculate Term Frequencies (TF)."""
import sys
import itertools


def reduce_one_group(key, group):
    """Reduce one group: Compute term frequency (TF)."""
    word_count = {}

    for line in group:
        __, word = line.strip().split("\t")
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    for x, count in word_count.items():
        print(f"{x}\t{key} {count}")


def keyfunc(line):
    """Extract key (term and doc_id) from the mapper output."""
    return line.partition("\t")[0]


def main():
    """Read sorted mapper output, group by (term, doc_id), and calculate TF."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)

    # for key, group in itertools.groupby(sys.stdin, keyfunc):
    #     for line in group:
    #         print(line)


if __name__ == "__main__":
    main()
