import yaml
from .application import Application
from technews_nlp_aggregator.nlp_model.common import TechArticlesCleaner

import logging


def cleanup(application):
    def convert_file(id, con):

        article_record = _.articleDatasetRepo.load_article_with_text(id)
        _.articleDatasetRepo.update_article_text(id, article_record["ATX_TEXT_ORIG"], con)

    def cleaned_text(title, text):

        text = article_cleaner.do_clean(text)
        text = _.tokenizer.sentence_tokenizer.clean_sentences(text)
        return "\n".join(text)

    _ =  application

    article_cleaner = TechArticlesCleaner()
    articleFilteredDF = _.articleLoader.articlesDF
    con = _.articleDatasetRepo.get_connection()
    count = 0
    for index, row in articleFilteredDF.iterrows():

        convert_file(row['article_id'], con)
        count += 1
        if (count % 100 == 0):
            print("Processed {} articles".format(count ) )

if __name__ == '__main__':
    import sys
    sys.path.append('..')

    config = yaml.safe_load(open('../config.yml'))
    application = Application(config, True)

    cleanup(application)
