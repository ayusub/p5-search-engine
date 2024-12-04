"""Handle search requests."""
import threading
import heapq
import flask
from flask import request
import requests
import search


@search.app.route("/", methods=["GET"])
def handle_search():
    """Handle search."""
    text = request.args.get('q', '')
    weight = request.args.get('w', '0.5')

    searched = text.strip() != ""

    context = {
        "query": text,
        "weight": weight,
        "searched": searched,
        "results": None,
    }

    if searched:
        combined_results = start_thread(text, weight)
    else:
        context["results"] = None
        return flask.render_template("index.html", **context)

    connection = search.model.get_db()
    cursor = connection.cursor()

    result_data = []
    for result in combined_results:
        docid = result['docid']
        data = cursor.execute(
            'SELECT title, summary, url FROM documents WHERE docid = ?',
            (docid,)).fetchone()

        result_data.append({
            'docid': docid,
            'title': data['title'],
            'summary': data['summary'],
            'url': data['url']

        })

    context["results"] = result_data

    return flask.render_template("index.html", **context)


def start_thread(text, weight):
    """Create thread to execute a request."""
    results = []

    urls = search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']

    print("URLs to query:", urls)

    threads = []

    for url in urls:
        thread = threading.Thread(target=fetch_results,
                                  args=(url, text, weight, results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    flattened_results = [item for sublist in results for item in sublist]
    # print("Flattened results for merging:", flattened_results)  # Debug
    combined_results = heapq.nlargest(
        10, flattened_results, key=lambda x: x['score'])
    # print("Top combined results:", combined_results)
    return combined_results


def fetch_results(url, text, weight, results):
    """Get results."""
    response = requests.get(url, params={'q': text, 'w': weight}, timeout=30)
    response.raise_for_status()  # Raise HTTP errors
    json_data = response.json()

    results.append(json_data["hits"])
