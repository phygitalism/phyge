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
        # то что ниже можно убрать
        self.id = self.storage.test_case_id
        self.path = self.storage.test_case_path  # нужен только в usi можно убрать
        self.urls = self.storage.get_urls()
        self.queries = self.storage.get_queries()
        self.articles = None
        self.values = None
        self.new_urls = self.get_new_urls()

        if self.new_urls:
            self.fetch_state = FetchState.NewArticle
        else:
            self.fetch_state = FetchState.OldArticle

    def get_new_urls(self):
        #db_urls = [x.get('url') for x in self.storage.get_urls()]
        urls_old = [x.get('url') for x in self.storage.get_urls_status()]
        sbuf = set(urls_old)
        urls_new = list()
        for url in self.urls:
            if url['url'] not in sbuf:
                urls_new.append(url)
        #new_urls = [x for x in db_urls if x not in sbuf]
        return urls_new

    def setup(self):  # загрузка текстов по новым ссылкам
        if self.fetch_state == FetchState.NewArticle:
            self.articles = self.article_fetcher.load_articles(self.storage, self.new_urls)
        else:
            self.articles = self.storage.get_articles()
        self.values = self.storage.get_words_list()

    #def uci_representation(self, path):
    #    pairs = zip(range(len(self.articles)), self.articles)
    #    data = dict((key, value.normalized_words) for key, value in pairs)
    #    bag_of_words = BagOfWordsModel(data)
    #    bag_of_words.to_uci(model_name='articles', save_folder=path + '/uci')