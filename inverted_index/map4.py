#!/usr/bin/env -S python3 -u
# """Map 3: Calculate Everything Else."""
# import sys

# # INPUT:  print(f"{doc['doc_id']}\t{key} {tf_idf} {tf_ik}")

# for line in sys.stdin:
#     # term k    
#     doc_id, rest = line.split("\t")
#     term, tf_idf, tf_ik = rest.split()
#     # # doc id 
#     # # print something here ? 
#     # # tf(ik) = k frequency in i
#     #         # num_docs = terms[k] + 1

#     #         # terms[k] += tf_ik, num_docs[k]`
#     print(f"{doc_id}\t{term} {tf_idf} {tf_ik}")
#     # print(line)
import sys

def main():
    for line in sys.stdin:
        # Strip whitespace and check for empty or malformed lines
        line = line.strip()
        if not line:
            continue
        
        try:
            # Split the input line into parts
            doc_id, rest = line.split("\t")
            term, tf_idf, tf_ik = rest.split()
            
            # Emit the transformed output
            print(f"{doc_id}\t{term} {tf_idf} {tf_ik}")
        
        except ValueError:
            # Handle unexpected line formats (optional)
            print(f"Skipping malformed line: {line}", file=sys.stderr)

if __name__ == "__main__":
    main()

 