from enum import Enum
from ArticleFetcher import ArticleFetcher
from Storage import Storage


class DownloadArticlesState(Enum):
    OldArticle, NewArticle = range(2)

    def __str__(self):
        return str(self.name)


class TestCase:
    def __init__(self, test_case_id):
        self.storage = Storage(test_case_id)
        self.article_fetcher = ArticleFetcher()
        self.id = self.storage.test_case_id
        self.path = self.storage.test_case_path
        self.urls = self.storage.get_urls()
        self.queries = self.storage.get_queries()
        self.articles = self.storage.get_articles()
        self.values = self.storage.get_words_df_json()
        self.dct = self.storage.save_dct_for_model()
        self.corpus = self.storage.get_corpus()
        self.fetch_state = DownloadArticlesState.OldArticle

    def setup(self):
        existing_urls = [article.url for article in self.articles]
        filtred_urls = [x for x in self.urls if x['url'] not in existing_urls]
        if len(filtred_urls) > 0:
            self.fetch_state = DownloadArticlesState.NewArticle
            self.downloaded_articles = self.article_fetcher.load_articles(filtred_urls)
            self.articles += self.downloaded_articles

        self.storage.save_articles(self.articles)
        self.values = self.storage.get_words_list()

    # def uci_representation(self, path):
    #    pairs = zip(range(len(self.articles)), self.articles)
    #    data = dict((key, value.normalized_words) for key, value in pairs)
    #    bag_of_words = BagOfWordsModel(data)
    #    bag_of_words.to_uci(model_name='articles', save_folder=path + '/uci')