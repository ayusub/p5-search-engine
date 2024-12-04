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
                docs_info = []
                for i in range(2, len(vals), 3):  # Start at index 2 and step by 3
                    doc_id = vals[i]
                    tf = float(vals[i + 1])
                    norm = float(vals[i + 2])
                    docs_info.append({"doc_id": doc_id, "tf": tf, "norm": norm})
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

    terms = [re.sub(r"[^a-zA-Z0-9]+", "", term).casefold() for term in query.split()]
    # clean query with stop words and inverted index ; TODO: write load funciton
    terms = [term for term in terms if term not in stopwords] #fix later
    print("cleaned query", file=sys.stderr)
    if not all(term in inverted_index for term in terms):
        print("ERROR: terms not in inverted index", file=sys.stderr)
        return flask.jsonify({"hits": []})

    doc_sets = [set(doc["doc_id"] for doc in inverted_index[term]["docs"]) for term in terms]
    documents = set.intersection(*doc_sets)

    if not documents:
        print("ERROR: no docs", file=sys.stderr)
        return flask.jsonify({"hits": []})
    
    query_vector = calculate_query(terms)

    for doc_id in documents:
        doc_vector = calculate_doc(doc_id, terms)
        tf_idf_score = calc_cosine_similarity(query_vector, doc_vector)
        # print(pagerank[doc_id], file=sys.stderr)
        print(weight, file=sys.stderr)
        print(tf_idf_score, file=sys.stderr)
        rank = pagerank.get(doc_id, 0)
        final_score = (weight * rank) + ((1 - weight) * tf_idf_score)
        hits.append({"docid": int(doc_id), "score": final_score})

    hits = sorted(hits, key=lambda x: x["score"], reverse=True)
    return flask.jsonify({"hits": hits})


def calculate_query(terms):
    """Normalize query vector"""
    # make query vector
    # print("calc query norm", file=sys.stderr)
    query_vector = []
    term_frequencies = Counter(terms)
    for term, q_tf in term_frequencies.items():
        if term in inverted_index: #make sure that both terms are in document 
            idf = inverted_index[term]['idf']
            query_vector.append(float(q_tf) * float(idf))
    
    query_nf = math.sqrt(sum(term ** 2 for term in query_vector))
    # normalize query vector
    query_vector = [val / query_nf for val in query_vector]
    return query_vector 

    
def calculate_doc(doc_id, terms):
    """Normalize document vector."""
    # print("calc doc norm", file=sys.stderr)
    doc_vector = []
    for term in terms:
        for doc in inverted_index[term]["docs"]:
            if doc['doc_id'] == doc_id:
                tf = doc['tf']
                idf = inverted_index[term]['idf']
                doc_vector.append(tf * idf)
                break
    doc_nf = math.sqrt(sum(val ** 2 for val in doc_vector))
    doc_vector = [val / doc_nf for val in doc_vector]
    return doc_vector
    

def calc_cosine_similarity(query_vector, doc_vector):
    """Compute the cosine similarity between query and document vectors."""
    print("cos", file=sys.stderr)
    return sum(q * d for q, d in zip(query_vector, doc_vector))