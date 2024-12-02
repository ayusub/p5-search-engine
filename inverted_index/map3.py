#!/usr/bin/env -S python3 -u
"""Map 3: Calculate Everything Else."""
import sys
import math

# JOB 3: tf-idf score, doc_id, tf fin doc, ....
# input: term : doc_id frequency

# terms = {}
# tf_ik = {}
# read input from previous job output directory ?
for line in sys.stdin:
    # term k
    term, rest = line.split("\t")
    doc_id, tf_ik = rest.split()
    # doc id 
    # print something here ? 
    # tf(ik) = k frequency in i
            # num_docs = terms[k] + 1

            # terms[k] += tf_ik, num_docs[k]`
    print(f"{term}\t{doc_id} {tf_ik}")

    # n(k) = number of docs with k
    

# # N = size of collection 
#     # get from output file from pipeline or smth 
# with open("total_document_count.txt", 'r', encoding="utf-8") as f:
#     collection_size = int(f.read().strip())
    
# # idf(k) = log(N/n(k)) -> inverse doc freq for term k in collection C
# inverse_doc_freq = {}
# for term, count in terms: 
#     idf_k = math.log10(collection_size/count)
#     inverse_doc_freq[term] = idf_k

# # w(ik) = tf-idf score in doc i: idf(k) * tf(ik)
# for key, value in tf_ik: 
#     w_ik = 

# # vals for map: 

# # |di| = Normalization factor for one document over every term  in that document*



# # Read the total document count from a file
# # N = read("total_document_count.txt")

# # for line in input:
# #     # Split input into term, n_t, and doc_id:term_frequency
# #     term, n_t, doc_tf = parse(line)
    
# #     # Parse doc_tf into doc_id and term_frequency
# #     doc_id, term_frequency = parse(doc_tf)
    
# #     # Convert n_t and term_frequency to integers or floats
# #     n_t = int(n_t)
# #     term_frequency = float(term_frequency)
    
# #     # Calculate IDF
# #     idf = log10(N / n_t)
    
# #     # Calculate TF-IDF
# #     tf_idf = term_frequency * idf
    
# #     # Emit TF-IDF for this term
# #     emit(f"{doc_id}\t{term}\t{tf_idf}")
    
# #     # Emit TF-IDF squared for normalization
# #     tf_idf_squared = tf_idf ** 2
# #     emit(f"{doc_id}\t{tf_idf_squared}")
