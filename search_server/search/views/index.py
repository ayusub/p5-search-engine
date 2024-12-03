"""Handle search requests"""
import flask
from flask import request
import search
import threading 

@search.app.route("/", methods=["GET"])
def handle_search():
    """Handle search."""
    text = request.args.get('q', '')
    range = request.args.get('w', '0.5')

    if not text: 
        context = {
            "query": text,
            "weight": range,
            "results": None
        }
        return flask.render_template("index.html", **context)
    
    context = {
        "query": text,
        "weight": range,
        "results": find_results(text, range),
    }
    return flask.render_template("index.html", **context)

def find_results():