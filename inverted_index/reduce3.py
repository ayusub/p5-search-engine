#!/usr/bin/env python3
"""Reduce 3: Calculate Everything Else."""
import sys
import math
import itertools


# INPUT FORMAT: print(f"{term}\t{doc_id} {tf_ik}")
# OUTPUT FORMAT: <term>\t<doc_id> <tf_idf_score/weight> <term_frequency> <normalization_factor>

values = {} 

"""
Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""

def reduce_one_group(key, group):
    """Reduce one group."""

    with open("total_document_count.txt", 'r', encoding="utf-8") as f:
        collection_size = int(f.read().strip())
    
    
    doc_list = []  # Temporary list to hold document data for the term

    # Process each line in the group
    for line in group:
        # print(line)
        term, rest = line.split("\t")  # Split term and the rest
        doc_id, tf_ik = rest.split()  # Split rest into doc_id and tf_ik

        # Add document data to the list
        doc_list.append({"doc_id": doc_id, "tf_ik": float(tf_ik)})

    # Store the term's data in the global dictionary
    values[key] = doc_list

    for key, doc_list in values.items(): 
        nk = len(doc_list)
        idf_k = math.log10(collection_size/nk)
   
        normalization_factor = 0
        for doc in doc_list:
            tf_ik = doc["tf_ik"]
            tf_idf = tf_ik * idf_k
            normalization_factor += tf_idf ** 2

            print(f"{key}\t{doc['doc_id']} {tf_idf} {tf_ik} {normalization_factor}")
 


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    # print("hi3")

    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)

    # N = size of collection 
    # get from output file from pipeline or smth 
    # with open("total_document_count.txt", 'r', encoding="utf-8") as f:
    #     collection_size = int(f.read().strip())
    
    # for key, doc_list in values.items(): 
    #     nk = len(doc_list)
    #     idf_k = math.log10(collection_size/nk)
   
    #     normalization_factor = 0
    #     for doc in doc_list:
    #         tf_ik = doc["tf_ik"]
    #         tf_idf = tf_ik * idf_k
    #         normalization_factor += tf_idf ** 2

    #         print(f"{key}\t{doc['doc_id']} {tf_idf} {tf_ik} {normalization_factor}")

    


if __name__ == "__main__":
    main()





# vals for map: 

# |di| = Normalization factor for one document over every term  in that document*
#OUTPUT FORMAT PLSZ
#<term>\t<doc_id> <tf_idf_score/weight> <term_frequency> <normalization_factor>

#seperate with space pls thx


# for line in input:
#     # Split input into term, n_t, and doc_id:term_frequency
#     term, n_t, doc_tf = parse(line)
    
#     # Parse doc_tf into doc_id and term_frequency
#     doc_id, term_frequency = parse(doc_tf)
    
#     # Convert n_t and term_frequency to integers or floats
#     n_t = int(n_t)
#     term_frequency = float(term_frequency)
    
#     # Calculate IDF
#     idf = log10(N / n_t)
    
#     # Calculate TF-IDF
#     tf_idf = term_frequency * idf
    
#     # Emit TF-IDF for this term
#     emit(f"{doc_id}\t{term}\t{tf_idf}")
    
#     # Emit TF-IDF squared for normalization
#     tf_idf_squared = tf_idf ** 2
#     emit(f"{doc_id}\t{tf_idf_squared}")
