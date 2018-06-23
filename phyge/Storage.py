import pandas as pd
import json
import os
from gensim import models

from ArticleSerializer import ArticleSerializer
from Models.PhygeVariables import PhyVariables
from Models.TestCase import TestCase
from Models.Query import Query


class Storage:
    def __init__(self, test_case_id):
        self.test_case_id = test_case_id
        self.test_case_path = PhyVariables.testCasePath
        self.tmp_path = PhyVariables.tmpPath
        self.urls_path = PhyVariables.urlsPath
        self.queries_path = PhyVariables.queriesPath
        self.articles_path = PhyVariables.articlesPath
        self.values_path = PhyVariables.valuesPath
        self.lsi_path = PhyVariables.lsiPath
        self.lda_path = PhyVariables.ldaPath
        self.w2v_path = PhyVariables.w2vPath

        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)

    def load_test_case(self):
        urls = []
        with open(self.urls_path, 'r', encoding="utf8") as json_file:
            data_urls = json.load(json_file)
        for article in data_urls:
            urls.append(dict(url=article.get('url'), language=article.get('language', '')))

        queries = self.__load_queries(self.queries_path)

        saved_articles, values = list(), None

        if os.path.isfile(self.articles_path):
            saved_articles = ArticleSerializer.deserialize(self.articles_path)

        if os.path.isfile(self.values_path):
            values = pd.read_csv(self.values_path, dtype='unicode')

        return TestCase(self.test_case_id, {'urls':  urls,
                                            'path': self.test_case_path,
                                            'queries': queries,
                                            'articles': saved_articles,
                                            'values': values})

    def __load_queries(self, queries_json_path) -> [Query]:
        if not os.path.isfile(queries_json_path):
            return list()

        with open(queries_json_path, 'r', encoding='utf8') as file:
            queries = json.load(file)
            return [Query(obj) for obj in queries]

    def load_LSI_model(self):
        print('\nLSI model loadind...')
        try:
            lsi = models.lsimodel.LsiModel.load(self.lsi_path)
            print('Loaded')
        except:
            print('Модель не найдена.')
            lsi = None
        return lsi

    def load_LDA_model(self):
        print('\nLDA model loading...')
        try:
            lda = models.ldamodel.LdaModel.load(self.lda_path)
            print('Loaded')
        except:
            print('Модель не найдена.')
            lda = None
        return lda

    def save_lsi_model(self, model):
        model.save(self.lsi_path)
        print('Model saved ')

    def save_lda_model(self, model):
        model.save(self.lda_path)
        print('Model saved ')
