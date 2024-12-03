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
    word_count = {}

    for line in group:
        doc_id, word = line.strip().split("\t")  # Split term and the rest 
        if line in word_count:
            word_count[word] += 1; 
        else: 
            word_count[word] = 1; 
            
    for x, count in word_count.items(): 
        print(f"{x}\t{key} {count}")


def keyfunc(line):
    """
    Extract key (term and doc_id) from the mapper output.
    """
    return line.partition("\t")[0]

def main():
    """
    Read sorted mapper output, group by (term, doc_id), and calculate TF.
    """
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
