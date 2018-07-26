
import pandas as pd
from gensim import corpora

from Models.PhygeArticle import AbstractArticle


class TrainingSample:
    def __init__(self, articles: [AbstractArticle]):
        self.articles = articles
        self.values = self.as_data_frame()
        self.dictionary = self.build_dictionary()
        self.corpus = self.get_corpus()

    def as_data_frame(self) -> pd.DataFrame:
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
