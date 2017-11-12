#################
#### imports ####
#################


from flask import Flask, render_template
from .util import read_int_from_form

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

import technews_nlp_aggregator.web.duplicate_articles
import technews_nlp_aggregator.web.compare_articles
import technews_nlp_aggregator.web.retrieve_similar
import technews_nlp_aggregator.web.retrieve_similar_url
import technews_nlp_aggregator.web.add_new_url
import technews_nlp_aggregator.web.show_groups
import technews_nlp_aggregator.web.sign_in



import technews_nlp_aggregator.web.statistics
import technews_nlp_aggregator.web.admin
