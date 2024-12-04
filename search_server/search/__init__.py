"""Initalize file."""
from flask import Flask

app = Flask(__name__)  # pylint: disable=invalid-name

import search.views  # noqa: E402  pylint: disable=wrong-import-position
import search.model  # noqa: E402  pylint: disable=wrong-import-position

app.config.from_object('search.config')
