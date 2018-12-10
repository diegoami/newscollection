from .util import read_int_from_form
from technews_nlp_aggregator.common.util import conv_to_date
from flask import render_template,  request, session, redirect, url_for
from .merge_tables import merge_sims_maps, retrieve_sims_map_with_dates
from .summary import get_highlighted_text

from . import app


@app.route('/add_urls_start')
def add_urls_start():
    if (session["signed_in"]):
        return render_template('add_urls.html')
    else:
        return redirect(url_for('show_groups'))



@app.route('/add_urls', methods=['POST'])
def add_urls():
    _ = app.application
    if request.method == 'POST':
        form = request.form
        if form:
            urls = form["urls"]
            lines = urls.split('\n')
            messages = _.articlesSpiderRepo.add_url_list(lines)
            return render_template('add_urls.html', messages=messages)
