
import traceback

from flask import request, render_template, session

from . import app

#


@app.route('/filterduplicates', methods=['POST'])
def filterduplicates():
    if request.method == 'POST':
        form = request.form
        if form:
            filterCriteria = form["filterCriteria"]
            session['filterCriteria'] = request.form['filterCriteria']
    return duplicates()

@app.route('/duplicates', defaults={'page_id': 1})
@app.route('/duplicates/<int:page_id>')
def duplicates(page_id=1):
    _ = app.application
    filter_criteria = "P_SCORE > {}  AND ( U_SCORE IS NULL)".format(_.threshold)
    messages = []
    paging_rate = 50
    back_forth = 6
    try:
        all_articles_DF = _.similarArticlesRepo.list_similar_articles(version=_.version, filter_criteria=filter_criteria )
        start, end = (page_id-1)*paging_rate, (page_id)*paging_rate
        if (len(all_articles_DF) > start):
            has_next = len(all_articles_DF) > end
            dup_articles_DF = all_articles_DF.iloc[start:min(end,len(all_articles_DF))]
            dup_articles = dup_articles_DF.to_dict(orient='records')

        else:
            dup_articles = []

            return render_template('duplicates.html', messages=['No articles found with this query'],
                                   filter_criteria=filter_criteria)
        how_many_pages = min(max((len(all_articles_DF) - end) // paging_rate, 1), back_forth)
        begin_page = max(1, page_id - back_forth)
        return render_template('duplicates.html', dup_articles=dup_articles, page_id=page_id, has_next=has_next, filter_criteria=filter_criteria, how_many_pages=how_many_pages, begin_page = begin_page)
    except:
        traceback.print_exc()
        return render_template('duplicates.html',  filter_criteria=filter_criteria, messages=['Could not execute query - filter criteria are not valid'])
