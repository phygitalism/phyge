import pandas as pd
from gensim import corpora
from DBController import DBController
from Models.PhygeArticle import BaseArticle


class TrainingSample:
    LIMIT = 10

    def __init__(self,articles):
        self.dictionary = self.build_dictionary()
        self.corpus = self.get_corpus()
        self.articles = articles

    def build_dictionary(self):
        documents = IterDocuments(limit=self.LIMIT)
        dct = corpora.Dictionary(documents)
        return dct

    def get_corpus(self):
        corpus = IterCorpus(my_dict=self.dictionary, limit=self.LIMIT)
        return corpus

    def get_documents(self):
        documents = IterDocuments(limit=self.LIMIT)
        return documents


class IterDocuments:
    def __init__(self, limit):
        self.limit = limit

    def __iter__(self):
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
        for id in range(self.limit):
            article = DBController.get_article(id)
            if article:
                yield self.dictionary.doc2bow(article['normalized_words'])
