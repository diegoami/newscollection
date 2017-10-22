import abc

class ArticleRepo:
    @abc.abstractmethod
    def load_articles(self):
        pass

    @abc.abstractmethod
    def save_articles(self):
        pass
