#################
#### imports ####
#################


from flask import Flask, render_template
from .util import read_int_from_form

from flask import request, render_template, session, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('show_groups'))

import technews_nlp_aggregator.web.duplicate_articles
import technews_nlp_aggregator.web.compare_articles
import technews_nlp_aggregator.web.retrieve_similar
import technews_nlp_aggregator.web.retrieve_similar_url
import technews_nlp_aggregator.web.add_new_url
import technews_nlp_aggregator.web.show_groups
import technews_nlp_aggregator.web.sign_in
import technews_nlp_aggregator.web.browse
import technews_nlp_aggregator.web.hide



import technews_nlp_aggregator.web.statistics
import technews_nlp_aggregator.web.admin
