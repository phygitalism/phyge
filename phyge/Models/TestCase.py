import pandas as pd

from Models.PhygeVariables import PhyVariables
from Models.BagOfWordsModel import BagOfWordsModel

from ArticleFetcher import ArticleFetcher
from ArticleSerializer import ArticleSerializer


class TestCase:
    def __init__(self, id, obj: dict):
        self.id = id
        self.path = obj.get('path', None)
        self.urls = obj.get('urls', list())
        self.articles = obj.get('articles', list())
        self.queries = obj.get('queries', list())
        self.values = obj.get('values', None)

    def setup(self):
        if len(self.articles) != len(self.urls):
            existing_urls = [article.downloaded_from_url for article in self.articles]
            filtred_urls = [x for x in self.urls if x not in existing_urls]

            article_fetcher = ArticleFetcher(filtred_urls)
            downloaded_articles = article_fetcher.fetch()

            self.articles += downloaded_articles

        ArticleSerializer.serialize(self.articles, self.path + '/tmp/' + PhyVariables.articlesFileKey)

        if self.values is None:
            self.values = self.__create_df_words()

        self.uci_representation(self.path + '/tmp/')

    def __create_df_words(self):
        columns = [pd.Series(article.normalized_words) for article in self.articles]
        pairs = zip(range(len(self.articles)), columns)
        data = dict((key, value) for key, value in pairs)

        df_words_in_doc = pd.DataFrame(data)
        df_words_in_doc.to_csv(str.format('{0}/test_{1}/{2}/{3}', PhyVariables.testsPath, str(self.id), '/tmp/',
                                          PhyVariables.valuesFileKey),
                               index=False,
                               encoding='utf8')
        return df_words_in_doc

    def uci_representation(self, path):
        pairs = zip(range(len(self.articles)), self.articles)
        data = dict((key, value.normalized_words) for key, value in pairs)

        bag_of_words = BagOfWordsModel(data)
        bag_of_words.to_uci(model_name='articles', save_folder=path + '/uci')
