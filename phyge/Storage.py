import pandas as pd
import json
import os
from gensim import corpora, models

from PhygeVariables import PhyVariables


class Storage:
    def __init__(self, test_case_id):
        self.test_case_id = test_case_id
        self.test_case_path = PhyVariables.testCasePath
        self.tmp_path = PhyVariables.tmpPath
        self.urls_path = PhyVariables.urlsPath
        self.urls_status_path = PhyVariables.urlsStatusPath
        self.queries_path = PhyVariables.queriesPath
        self.articles_path = PhyVariables.articlesPath
        self.values_path = PhyVariables.valuesPath
        self.lsi_path = PhyVariables.lsiPath
        self.lda_path = PhyVariables.ldaPath
        self.w2v_path = PhyVariables.w2vPath
        self.dct_path = PhyVariables.dctPath

        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)

    # сохранение и зашрузка файлов на комп все в storage
    def get_urls(self):
        urls = []
        if not os.path.isfile(self.urls_path):
            return list()
        with open(self.urls_path, 'r', encoding="utf8") as json_file:
            data_urls = json.load(json_file)
            for u in data_urls:
                urls.append(dict(url=u.get('url'), language=u.get('language', '')))
        return urls

    def get_urls_status(self):
        urls = []
        if not os.path.isfile(self.urls_status_path):
            return list()
        with open(self.urls_status_path, 'r', encoding="utf8") as json_file:
            data_urls = json.load(json_file)
            for u in data_urls:
                urls.append(dict(url=u.get('url'), status=u.get('status', '')))
        return urls

    def get_new_urls(self):
        db_urls = [x.get('url') for x in self.get_urls()]
        old_urls = [x.get('url') for x in self.get_urls_status()]
        sbuf = set(old_urls)
        new_urls = [x for x in db_urls if x not in sbuf]
        return new_urls

    # во время скачивания страница может не загрузиться, может не распарситься
    # зоздается файл с информацией о загрузке текста по ссылкам
    # дозаписываем информацию о скачивании по новым ссылкам в файл
    def save_urls_status(self, urls_status_new):
        urls_status = []
        if os.path.isfile(self.urls_status_path):
            urls_status = self.get_urls_status()
        urls_status = urls_status + urls_status_new
        with open(self.urls_status_path, 'w', encoding="utf8") as file:
            s = json.dumps(urls_status, indent=2, ensure_ascii=False)
            file.write(s)

    def save_articles(self, articles_list):
        articles = []
        if os.path.isfile(self.articles_path):
            articles = self.get_articles()
        articles = articles + articles_list
        with open(self.articles_path, 'w', encoding="utf8") as file:
            s = json.dumps(articles, indent=2, ensure_ascii=False)
            file.write(s)

    def get_articles(self):
        saved_articles = list()
        with open(self.articles_path, 'r', encoding='utf8') as file:
            data_articles = json.load(file)
            for a in data_articles:
                saved_articles.append(a)
        return saved_articles

    def get_words_df_json(self):
        articles_list = self.get_articles()
        columns = [pd.Series(article["normalized_words"]) for article in articles_list]
        pairs = zip(range(len(articles_list)), columns)
        data = dict((key, value) for key, value in pairs)
        df_words_in_doc = pd.DataFrame(data)
        # csv не используется, можно убрать, чисто для наглядности
        df_words_in_doc.to_csv(self.values_path, index=False, encoding='utf8')
        return df_words_in_doc

    def get_words_list(self):
        df = self.get_words_df_json()
        words_list = []
        for columns in df.columns:
            words_list.append(df[columns].dropna().tolist())
        return words_list

    def get_queries(self):
        if not os.path.isfile(self.queries_path):
            return list()
        queries = list()
        with open(self.queries_path, 'r', encoding='utf8') as file:
            data_queries = json.load(file)
            for q in data_queries:
                queries.append(q)
        return queries

    # сохраняет словарь для модели
    def save_dct(self):
        documents = self.get_words_list()
        dct = corpora.Dictionary(documents)
        dct.save(self.dct_path)
        return dct

    # загружает словарь для модели
    def get_dct(self):
        if os.path.isfile(self.dct_path):
            dct = corpora.Dictionary.load(self.dct_path)
        else:
            dct = self.save_dct()
        return dct

    # загружаем корпус
    def get_corpus(self):
        dct = self.get_dct()
        documents = self.get_words_list()
        return [dct.doc2bow(doc) for doc in documents]

    # загружаем модель из файла
    def get_model(self, model_name, load_path):
        print('%s model loading...' % model_name)
        if model_name == 'lsi':
            load_func = models.lsimodel.LsiModel.load
        elif model_name == 'lda':
            load_func = models.ldamodel.LdaModel.load
        else:
            load_func = models.Word2Vec.load
        try:
            model = load_func(load_path)
            print('Loaded')
        except:
            print('Модель не найдена.')
            model = None
        return model

    def save_model(self, model, save_path):
        model.save(save_path)