#!/usr/bin/env -S python3 -u
"""Map 4: Segment."""

import sys

for line in sys.stdin:
    #this should get term which hypothetically is the key in output3
    term, value = line.rstrip().split("\t")
    
    # Extract the document ID (assumes it's the first word in value)- change 
    doc_id = int(value.split()[0])
    
    # Calculate the partition key
    partition_key = int(doc_id) % 3
    
    # Print the partition key and the modified value
    print(f"{partition_key}\t{term}\t{value}")
