#!/usr/bin/env -S python3 -u
"""Map 4: Segment."""

import sys
# import logging

# logging.basicConfig(level=logging.DEBUG)

for line in sys.stdin:
    split = line.rstrip().split("\t")

    # Extract the document ID (assumes it's the first word in value)- change
    term = split[0]
    rest = split[1]

    # doc_id = rest.split()[0]
    doc_id = rest.split()[0].strip()
    # Calculate the partition key
    partition_key = int(doc_id) % 3
    # logging.debug("key %d", partition_key)

    # Print the partition key and the modified value
    print(f"{partition_key}\t{term}\t{rest}")
