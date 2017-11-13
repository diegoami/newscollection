from .util import read_int_from_form
from technews_nlp_aggregator.common.util import conv_to_date
from flask import render_template,  request, session
from .merge_tables import merge_sims_maps, retrieve_sims_map_with_dates
from .summary import get_highlighted_text

from . import app


@app.route('/add_new_url_start')
def add_new_url_start():
    if (session["signed_in"]):
        return render_template('add_new_url.html')
    else:
        return render_template('home.html')

@app.route('/add_new_url', methods=['POST'])
def add_new_url():
    _ = app.application
    if request.method == 'POST':
        form = request.form
        if form:
            article = {}
            article["text"] = text = form["article_text"]
            article["title"] = title = form["article_title"]
            article["url"] = url = form["article_url"]
            n_articles = read_int_from_form(form, 'n_articles')
            date_s = form["article_date_s"]
            messages = []
            if not text or len(text.strip()) == 0:
                messages.append('Please enter the text of a technical article')
            if not title or len(title.strip()) == 0:
                messages.append('Please enter a title')
            if not date_s or len(date_s.strip()) == 0:
                messages.append('Please enter a date')

            if not url or len(url.strip()) == 0:
                messages.append('Please enter an url')
            if date_s:
                article["date"] = date = conv_to_date(date_s)
                if not date:
                    messages.append('Date is invalid (Format YYYY-MM-DD is accepted)')

            if (len(messages) > 0):
                return render_template('add_new_url.html', messages=messages)
            else:
                article_id = _.articleDatasetRepo.save_article( article, text)
                saved_article = _.articleDatasetRepo.load_article_with_text(article_id)
                saved_text = saved_article['ATX_TEXT']
                tdf_sims_map = retrieve_sims_map_with_dates(_.tfidfFacade, text=text, n_articles=n_articles)
                doc2vec_sims_map = retrieve_sims_map_with_dates(_.doc2VecFacade, text=text, n_articles=n_articles)
                tokens = _.tfidfFacade.get_tokenized(doc=text, title=title)
                summaries = _.summaryFacade.summarize_text(doc=text, title=title)
                summary_text = get_highlighted_text(summaries)
                related_articles = merge_sims_maps(tdf_sims_map, doc2vec_sims_map, _.articleLoader, n_articles=n_articles)
                return render_template('add_new_url.html', articles=related_articles[:n_articles], tokens=tokens,
                                       A=saved_article, summary_text=summary_text, n_articles=n_articles )
