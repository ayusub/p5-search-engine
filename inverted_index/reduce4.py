#!/usr/bin/env python3
"""Reduce 3: Calculate Everything Else."""
import sys
import math
import itertools


# INPUT FORMAT: print(f"{term}\t{doc_id} {tf_ik}")
# OUTPUT FORMAT: <term>\t<doc_id> <tf_idf_score/weight> <term_frequency> <normalization_factor>

"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""


# add dict to make faster 

# if else statement, key for dict is doc_id 
def reduce_one_group(key, group):
    """Reduce one group."""

    normalization_factor = 0 

    group = list(group)

    for line in group:
        # print("here")
        line = line.strip()
        # print(line)
        # parts = line.split(" ")
        
        # if len(parts) != 3:
        #     print(f"Skipping malformed line: {line}")
        #     continue  # Skip malformed lines
        doc_id, rest = line.split("\t")
        term, tf_idf, tf_ik = rest.split()
        normalization_factor += math.pow(float(tf_idf), 2)


    for line in group: 
        line = line.strip()
        # print("here")
        doc_id, rest = line.split("\t")
        term, tf_idf, tf_ik = rest.split()
        print(f"{term}\t{doc_id} {tf_idf} {tf_ik} {normalization_factor}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    # for key, group in itertools.groupby(sys.stdin, keyfunc):
        # print("key: ")
        # print(key)
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



