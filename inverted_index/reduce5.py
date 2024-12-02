#!/usr/bin/env python3
"""
Final Reducer for Inverted Index.
"""

import sys
import itertools

def reduce_one_group(key, group):

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

        # Append document-specific details to the term's list
        # term_data[term].append((doc_id, tf, norm, idf))
        # print(f"debug: {term} {term_data[term]}")
        
        # if term in duplicates: 
        #     # output = f"{doc_id} {tf} {norm}"
        #     print(f"{doc_id} {tf} {norm}")
        # else: 
        #     # output = f"{term} {idf} {doc_id} {tf} {norm}"
        #     print()
        #     print(f"{term} {idf} {doc_id} {tf} {norm}", end="")
        #     # duplicates[term] = 1

    

        # if term in duplicates:
        #     duplicates[term] += f" {doc_id} {tf} {norm}"  # Append to the existing value
        # else:
        #     duplicates[term] = f"{idf} {doc_id} {tf} {norm}"  # Start a new entry

        # for term, output in duplicates.items():
        #     print(f"{term} {output}")

    # Process and output results for each term
    # for term in term_data.keys():  # Sort terms lexicographically
    # #     # doc_list = sorted(term_data[term], key=lambda x: x[0])  # Sort by doc_id

    # #     output = f"{term} {idf}"
    # #     # for doc in doc_list:
    # #         output += f" {doc_id} {tf} {norm}"

    # #     print(output.rstrip())

    #     print(f"{term} {idf} {doc_id} {tf} {norm}")


def keyfunc(line):
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


    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)

if __name__ == "__main__":
    main()
