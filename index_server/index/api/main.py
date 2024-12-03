"""Main index."""

import flask
import index
import json
import re
import sys
import math
import os
from collections import Counter

inverted_index = {}
pagerank = {}
stopwords = set()

#load index here
def load_index():
    """Load the inverted index,stopwords, pagerank."""
    path_inverted_index = os.path.join(
        "./index_server/index/inverted_index", index.app.config["INDEX_PATH"]
    )
    # print(path_inverted_index, file=sys.stderr)
    path_stopwords = os.path.join("./index_server/index/stopwords.txt")

    path_pagerank = os.path.join("./index_server/index/pagerank.out")
    
   
    #open and add to dict 
    with open(path_inverted_index,"r", encoding='utf-8') as f:
        for line in f:
                vals = [val.strip() for val in line.split()]
                term = vals[0]
                # print(line[1], file=sys.stderr)
                idf = float(vals[1])
                docs_info = {}
                for i in range(2, len(vals), 3):  # Start at index 2 and step by 3
                    doc_id = vals[i]
                    tf = float(vals[i + 1])
                    norm = float(vals[i + 2])
                    docs_info[doc_id] = {"tf": tf, "norm": norm}
                inverted_index[term] = {"idf": idf, "docs": docs_info}
                
    with open(path_stopwords, "r", encoding='utf-8') as f:
        stopwords = set(word.strip() for word in f)
    
    with open(path_pagerank, "r", encoding ='utf-8') as f:
        for line in f:
            doc_id, rank = line.split(',')
            pagerank[doc_id] = float(rank)


@index.app.route('/api/v1/', methods=["GET"])
def get_index():
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@index.app.route("/api/v1/hits/", methods=["GET"])
def get_hits():
    """Return a list of hits with doc ID and score."""
    hits = []
    query = flask.request.args.get("q", type=str)
    weight = flask.request.args.get("w", type=float, default=0.5)

    terms = query.split()
    for term in terms:
        term = re.sub(r"[^a-zA-Z0-9 ]+", "", term)
        term = term.casefold()
        
    # clean query with stop words and inverted index ; TODO: write load funciton
    terms = [term for term in terms if term not in stopwords] #fix later
    print("cleaned query", file=sys.stderr)
    if not all(term in inverted_index for term in terms):
        print("ERROR: terms not in inverted index", file=sys.stderr)
        return flask.jsonify({"hits": []})
    # to check for IDF = 0????? terms = [term for term in query_terms if term in inverted_index and inverted_index[term]['idf'] > 0]

    #both terms are in document 
    doc_sets = [set(inverted_index[term]["docs"].keys()) for term in terms]
    
    documents = set.intersection(*doc_sets)

    if not documents:
        print("ERROR: no docs", file=sys.stderr)
        return flask.jsonify({"hits": []})
    
    query_vector = calculate_query_vector(terms)
    doc_nf = {}
    for term in terms:
        for doc_id in inverted_index[term]["docs"]:
            doc_nf[doc_id] = math.sqrt(inverted_index[term]["docs"][doc_id]["norm"])

    for doc_id in documents:
        doc_vector = calculate_doc_vector(doc_id, terms)
        dot_product = calc_cosine_similarity(query_vector, doc_vector)
        query_nf = math.sqrt(sum(pow(term, 2) for term in query_vector))
        tf_idf_score = dot_product / (abs(query_nf) * abs(doc_nf[doc_id]))
        # print(pagerank[doc_id], file=sys.stderr)
        print(weight, file=sys.stderr)
        print(tf_idf_score, file=sys.stderr)
        rank = pagerank.get(doc_id, 0)
        final_score = (weight * rank) + ((1 - weight) * tf_idf_score)
        hits.append({"docid": int(doc_id), "score": final_score})

    hits = sorted(hits, key=lambda x: x["score"], reverse=True)
    hits = hits[:min(10, len(hits))]
    return flask.jsonify({"hits": hits})


def calculate_query_vector(terms):
    """Normalize query vector"""
    # make query vector
    print("calc query norm", file=sys.stderr)
    query_vector = []
    term_frequencies = Counter(terms)
    for term, q_tf in term_frequencies.items():
        if term in inverted_index:
            idf = inverted_index[term]['idf']
            query_vector.append(float(q_tf) * float(idf))
    
    # query_nf = math.sqrt(sum(pow(term, 2) for term in query_vector))
    # query_vector = [val / query_nf for val in query_vector]
    return query_vector 

    
def calculate_doc_vector(doc_id, terms):
    """Normalize document vector."""
    print("calc doc norm", file=sys.stderr)
    doc_vector = []
    for term in terms:
        if doc_id in inverted_index[term]["docs"]:
            tf = inverted_index[term]["docs"][doc_id]["tf"]
            idf = inverted_index[term]['idf']
            doc_vector.append(tf * idf)

    # doc_nf = math.sqrt(sum(pow(val, 2) for val in doc_vector))
    # doc_vector = [val / doc_nf for val in doc_vector]
    return doc_vector
    

def calc_cosine_similarity(query_vector, doc_vector):
    """Compute the cosine similarity between query and document vectors."""
    print("cos", file=sys.stderr)
    return sum(q * d for q, d in zip(query_vector, doc_vector))