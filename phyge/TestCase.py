from ArticleFetcher import ArticleFetcher
from Storage import Storage

from enum import Enum


class FetchState(Enum):
    OldArticle, NewArticle = range(2)

    def __str__(self):
        return str(self.name)


class TestCase:
    def __init__(self, test_case_id):
        self.storage = Storage(test_case_id)
        self.article_fetcher = ArticleFetcher()
        self.new_urls = self.get_new_urls()
        # то что ниже можно убрать
        self.id = self.storage.test_case_id
        self.path = self.storage.test_case_path  # нужен только в usi можно убрать
        self.articles = None
        self.urls = None
        self.queries = None
        self.values = None

        if self.new_urls:
            self.fetch_state = FetchState.NewArticle
        else:
            self.fetch_state = FetchState.OldArticle

    def get_new_urls(self):
        db_urls = [x.get('url') for x in self.storage.get_urls()]
        old_urls = [x.get('url') for x in self.storage.get_urls_status()]
        sbuf = set(old_urls)
        new_urls = [x for x in db_urls if x not in sbuf]
        return new_urls

    def setup(self):  # загрузка текстов по новым ссылкам
        if self.fetch_state == FetchState.NewArticle:
            self.articles = self.article_fetcher.load_articles(self.storage, self.new_urls)
        # то что ниже можно убрать
        else:
            self.articles = self.storage.get_articles()
        self.urls = self.storage.get_urls()
        self.queries = self.storage.get_queries()
        self.values = self.storage.get_words_list()

    #def uci_representation(self, path):
    #    pairs = zip(range(len(self.articles)), self.articles)
    #    data = dict((key, value.normalized_words) for key, value in pairs)
    #    bag_of_words = BagOfWordsModel(data)
    #    bag_of_words.to_uci(model_name='articles', save_folder=path + '/uci')
