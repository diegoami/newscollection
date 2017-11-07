#################
#### imports ####
#################


from flask import Flask, render_template

from .util import read_int_from_form

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')



import technews_nlp_aggregator.web.retrieve_similar
import technews_nlp_aggregator.web.analyze_articles

import technews_nlp_aggregator.web.statistics
from .util import enclose_with_span, highlight_entities