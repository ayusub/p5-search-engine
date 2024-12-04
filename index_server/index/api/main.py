"""Main index."""
import re
import sys
import math
import os
from collections import Counter
import flask
import index

inverted_index = {}
pagerank = {}
stopwords = set()


# load index here
def load_index():
    """Load the inverted index,stopwords, pagerank."""
    path_inverted_index = os.path.join(
        "./index_server/index/inverted_index", index.app.config["INDEX_PATH"]
    )

    path_stopwords = os.path.join("./index_server/index/stopwords.txt")

    path_pagerank = os.path.join("./index_server/index/pagerank.out")

    # open and add to dict
    with open(path_inverted_index, "r", encoding='utf-8') as f:
        for line in f:
            vals = [val.strip() for val in line.split()]
            term = vals[0]
            # print(line[1], file=sys.stderr)
            docs_info = {}
            for i in range(2, len(vals), 3):
                doc_id = vals[i]
                docs_info[doc_id] = {
                    "tf": float(vals[i + 1]),
                    "norm": float(vals[i + 2])
                }
            inverted_index[term] = {"idf": float(vals[1]), "docs": docs_info}

    with open(path_stopwords, "r", encoding='utf-8') as f:
        stopwords.update(word.strip() for word in f)

    with open(path_pagerank, "r", encoding='utf-8') as f:
        for line in f:
            doc_id, rank = line.split(',')
            pagerank[doc_id] = float(rank)


@index.app.route('/api/v1/', methods=["GET"])
def get_index():
    """Return a list of services available."""
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
    terms = [
        re.sub(r"[^a-zA-Z0-9]+", "", term).casefold()
        for term in terms if re.sub(r"[^a-zA-Z0-9]+", "", term).strip()
    ]
    terms = [term for term in terms if term not in stopwords]
    # print(f"Filtered terms: {terms}", file=sys.stderr)
    # print(f"Stopwords loaded: {stopwords}", file=sys.stderr)
    if not all(term in inverted_index for term in terms):
        print("ERROR: terms not in inverted index", file=sys.stderr)
        return flask.jsonify({"hits": []})

    terms = [
        term for term in terms if term in inverted_index
        and inverted_index[term]['idf'] != 0
    ]

    documents = get_documents(terms)
    if not documents:
        return flask.jsonify({"hits": []})

    hits = calculate_scores(terms, documents, weight)
    return flask.jsonify({"hits": hits})


def get_documents(terms):
    """Find documents containing all query terms."""
    doc_sets = [set(inverted_index[term]["docs"].keys()) for term in terms]
    return set.intersection(*doc_sets)


def calculate_query_vector(terms):
    """Normalize query vector."""
    # print("calc query norm", file=sys.stderr)
    query_vector = []
    term_frequencies = Counter(terms)
    for term, q_tf in term_frequencies.items():
        if term in inverted_index:
            idf = inverted_index[term]['idf']
            query_vector.append(float(q_tf) * float(idf))
    return query_vector


def calculate_doc_vector(doc_id, terms):
    """Normalize document vector."""
    # print("calc doc norm", file=sys.stderr)
    doc_vector = []
    for term in terms:
        if doc_id in inverted_index[term]["docs"]:
            tf = inverted_index[term]["docs"][doc_id]["tf"]
            idf = inverted_index[term]['idf']
            doc_vector.append(tf * idf)
    return doc_vector


def calc_cosine_similarity(query_vector, doc_vector):
    """Compute the cosine similarity between query and document vectors."""
    # print("cos", file=sys.stderr)
    return sum(q * d for q, d in zip(query_vector, doc_vector))


def calculate_scores(terms, documents, weight):
    """Calculate scores for relevant documents."""
    query_vector = calculate_query_vector(terms)
    doc_nf = {
        doc_id: math.sqrt(inverted_index[term]["docs"][doc_id]["norm"])
        for term in terms for doc_id in inverted_index[term]["docs"]
    }

    hits = []
    for doc_id in documents:
        doc_vector = calculate_doc_vector(doc_id, terms)
        dot_product = calc_cosine_similarity(query_vector, doc_vector)
        query_nf = math.sqrt(sum(pow(term, 2) for term in query_vector))
        tf_idf_score = dot_product / (abs(query_nf) * abs(doc_nf[doc_id]))
        rank = pagerank.get(doc_id, 0)
        final_score = (weight * rank) + ((1 - weight) * tf_idf_score)
        hits.append({"docid": int(doc_id), "score": final_score})

    hits.sort(key=lambda x: x["score"], reverse=True)
    return hits[:10]
