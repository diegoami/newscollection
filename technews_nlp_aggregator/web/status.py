from flask import render_template,  request
from .summary import get_highlighted_text
from technews_nlp_aggregator.web.summary import convert_summary
from . import app
from flask import helpers

@app.route('/status')
def status():
    return helpers.make_response()