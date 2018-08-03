import pandas as pd
from gensim import corpora
from DBController import DBController
from Models.PhygeArticle import BaseArticle


class TrainingSample:
    LIMIT = 100

    def __init__(self):
        self.dictionary = self.build_dictionary()
        self.corpus = self.get_corpus()
        self.articles = DBController.get_all_articles()  # НЕ СООТВЕТСВУЕТ ДЕЙСТВИТЕЛЬНОСТИ

    def build_dictionary(self):
        documents = IterDocuments(limit=self.LIMIT)
        dct = corpora.Dictionary(documents)
        return dct

    def get_corpus(self):
        corpus = IterCorpus(my_dict=self.dictionary, limit=self.LIMIT)
        return corpus


class IterDocuments:
    def __init__(self, limit):
        self.limit = limit
        # self.articles = DBController.get_all_articles()
        # print(type(self.articles))

    def __iter__(self):
        # for article in self.articles:
        for id in range(self.limit):
            article = DBController.get_article(id)
            if article:
                yield article['normalized_words']


class IterCorpus:
    def __init__(self, my_dict, limit):
        self.dictionary = my_dict
        self.limit = limit
        self.articles = DBController.get_all_articles()

    def __iter__(self):
        # for article in self.articles:
        for id in range(self.limit):
            article = DBController.get_article(id)
            if article:
                yield self.dictionary.doc2bow(article['normalized_words'])