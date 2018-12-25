
from flask import render_template

from technews_nlp_aggregator.web.summary import convert_summary
from . import app


@app.route('/show_report')
def show_report():
    _ = app.application
    model_repo = _.model_repo
    scrape_repo = _.scrape_repo
    articlesSpiderRepo = _.articlesSpiderRepo
    model_performances = model_repo.load_model_performances()
    scrape_reports = scrape_repo.load_report()
    feature_reports = model_repo.load_feature_reports()
    urls_queued = articlesSpiderRepo.retrieve_urls_queued()
    return render_template('show_report.html', model_performances=model_performances, scrape_reports=scrape_reports,
                           urls_queued=urls_queued, feature_reports=feature_reports,
                           model_version=_.model_version, frontend_version=_.frontend_version)
