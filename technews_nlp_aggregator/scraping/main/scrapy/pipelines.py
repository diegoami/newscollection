import logging

class Pipeline(object):
    successfully_crawled = {}
    items_added = []
    def process_item(self, item, spider):

        if (len(item["title"]) >= 10) and (len(item["text"]) >= 600) and item["date"]:
            logging.info("Found url to add: {}".format(item["url"]))
            spider.article_repo.save_article(  item, item["text"])
            if spider.url_list:
                spider.article_repo.update_to_crawled(item["url"])

            self.successfully_crawled[spider.name] = self.successfully_crawled.get(spider.name,0) + 1
            self.items_added.append(item)

        else:
            logging.warning("Could not add url : {} (date: {}, len(text) : {})".format(item["url"], item["date"], len(item["text"])))

        return item