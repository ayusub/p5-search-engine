"""Main index."""

import flask
import index

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
    #SOME OF THIS SHOULD BE MODULATED INTO SMALLER FUNCS
    # # Step 1: Initialize variables
    # get query and weight using flask request args 
    # # Step 2: Search inverted index for matching documents
    # FOR term IN terms:
    #     matching_documents = lookup_inverted_index(term)  # Get all documents containing the term
    #     idf = compute_idf(term)                          # Calculate IDF for the term

    #     FOR document IN matching_documents:
    #         doc_id = document["doc_id"]                  # Extract document ID
    #         term_frequency = document["tf"]              # Extract term frequency in the document
    #         tf_idf_score = term_frequency * idf          # Compute TF-IDF for the term in this document

    #         IF doc_id NOT IN results:
    #             results[doc_id] = {"tf_idf": 0, "pagerank": get_pagerank(doc_id)}  # Initialize scores for the document

    #         results[doc_id]["tf_idf"] += tf_idf_score    # Accumulate TF-IDF scores for the document

    # # Step 3: Compute final scores
    # hits = []                                            # List to store the final results
    # FOR doc_id, scores IN results.items():
    #     tf_idf = scores["tf_idf"]
    #     pagerank = scores["pagerank"]

    #     # Calculate weighted score
    #     final_score = (weight * pagerank) + ((1 - weight) * tf_idf)

    #     # Append the document and its score to the hits list
    #     hits.append({"docid": doc_id, "score": final_score})

    # # Step 4: Sort hits by score in descending order
    # hits = sort(hits, key="score", descending=True)

    # # Step 5: Return the sorted results
    # RETURN hits
