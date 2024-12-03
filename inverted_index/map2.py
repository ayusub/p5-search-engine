#!/usr/bin/env -S python3 -u
"""Map 2: Calculate Term Frequencies (TF)."""

import sys
import re
#need to unCHATGPT this specifcally 
# Load stopwords into a set for faster lookups
stopwords = {}
with open("stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f)

for line in sys.stdin:
    # Parse input: split by TAB to separate doc_id and content
    doc_id, content = line.strip().split("\t", 1)

    # Split content into individual words
    words = content.split()

    for word in words:
        # Skip stopwords
        if word not in stopwords:
            word = word.casefold()
            word = re.sub(r"[^a-zA-Z0-9 ]+", "", word)
            if word not in stopwords:
                # Emit doc_id, word, and a count of 1
                print(f"{doc_id}\t{word}")
