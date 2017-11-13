import logging

class Pipeline(object):
    def process_item(self, item, spider):

        if (len(item["title"]) >= 10) and (len(item["text"]) >= 600) and item["date"]:
            logging.info("Found url to add: {}".format(item["url"]))
            spider.article_repo.save_article(  item, item["text"])
        else:
            logging.warning("Could not add url : {}".format(item["url"]))
        return item