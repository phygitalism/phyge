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
        self.test_case_path = str.format('{0}/test_{1}', PhyVariables.testsPath, self.test_case_id)
        self.tmp_path = (self.test_case_path + '/tmp/')
        self.lsi_path = self.tmp_path + PhyVariables.modelLsiKey
        self.lda_path = self.tmp_path + PhyVariables.modelLdaKey

    def load_test_case(self):
        self.test_case_path = str.format('{0}/test_{1}', PhyVariables.testsPath, self.test_case_id)
        tmp_path = (self.test_case_path + '/tmp/')
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        urls = []
        with open(self.test_case_path + '/' + PhyVariables.urlsFileKey, 'r', encoding="utf8") as json_file:
            data_urls = json.load(json_file)
        for article in data_urls:
            urls.append(article.get('url'))

        queries = self.__load_queries(self.test_case_path + '/' + PhyVariables.queriesFileKey)

        saved_articles, values = list(), None

        if os.path.isfile(self.tmp_path + PhyVariables.articlesFileKey):
            saved_articles = ArticleSerializer.deserialize(tmp_path + PhyVariables.articlesFileKey)

        if os.path.isfile(self.tmp_path + PhyVariables.valuesFileKey):
            values = pd.read_csv(self.tmp_path + PhyVariables.valuesFileKey, dtype='unicode')

        return TestCase(self.test_case_id, {'urls': urls,
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
