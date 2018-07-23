from enum import Enum
import re
import pandas as pd

from DBController import DBController
from Storage import Storage
from TextNormalizer import TextNormalizer
from Models.PhygeArticle import PhyArticle

from gensim import corpora


class DownloadArticlesState(Enum):
    OldArticle, NewArticle = range(2)

    def __str__(self):
        return str(self.name)


class TrainingSample:
    def __init__(self):
        # self.storage = Storage(test_case_id)
        self.articles = DBController.get_all_articles()
        self.values = self.as_dataframe()
        self.dictionary = self.build_dictionary()
        self.corpus = self.get_corpus()

    def as_dataframe(self) -> pd.DataFrame:
        columns = [pd.Series(article.normalized_words) for article in self.articles]
        pairs = zip(range(len(self.articles)), columns)
        data = dict((key, value) for key, value in pairs)
        return pd.DataFrame(data)

    @property
    def get_documents(self):
        documents = []
        for column in self.values.columns:
            documents.append(self.values[column].dropna().tolist())
        return documents

    def build_dictionary(self):
        documents = self.get_documents
        dct = corpora.Dictionary(documents)
        return dct

    def get_corpus(self):
        documents = self.get_documents
        corpus = [self.dictionary.doc2bow(doc) for doc in documents]
        return corpus
