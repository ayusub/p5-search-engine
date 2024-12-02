#!/usr/bin/env -S python3 -u
"""Map 4: Segment."""

import sys

for line in sys.stdin:
    #this should get term which hypothetically is the key in output3
    # print(f"{key}\t{doc['doc_id']} {w_ik} {tf_ik} {normalization_factor}")

    # Larry	67613335 0.47712125471966244 1.0 0.227644691705265
    #   print(f"{key}\t{doc['doc_id']} {w_ik} {tf_ik} {normalization_factor}")
   

    split = line.rstrip().split("\t")
    
    # Extract the document ID (assumes it's the first word in value)- change 
    term = split[0]
    rest = split[1]

    doc_id = rest.split()[0]  
    
    # Calculate the partition key
    partition_key = int(doc_id) % 3
    
    # Print the partition key and the modified value
    print(f"{partition_key}\t{term}\t{rest}")
