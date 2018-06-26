import pandas as pd
import json
import os
from gensim import corpora, models

from PhygeVariables import PhyVariables


class Storage:
    def __init__(self, test_case_id):
        self.test_case_id = test_case_id
        self.test_case_path = str.format('{0}/test_{1}', PhyVariables.testsDir, PhyVariables.currentTestKey)
        self.tmp_path = self.test_case_path + '/tmp'
        self.urls_path = os.path.join(self.test_case_path, PhyVariables.urlsFileKey)
        self.urls_status_path = os.path.join(self.tmp_path, PhyVariables.urlsStatusFileKey)
        self.queries_path = os.path.join(self.test_case_path, PhyVariables.queriesFileKey)
        self.articles_path = os.path.join(self.tmp_path, PhyVariables.articlesFileKey)
        self.values_path = os.path.join(self.tmp_path, PhyVariables.valuesFileKey)
        self.lsi_path = os.path.join(self.tmp_path, PhyVariables.modelLsiKey)
        self.lda_path = os.path.join(self.tmp_path, PhyVariables.modelLdaKey)
        self.w2v_path = os.path.join(self.tmp_path, PhyVariables.modelW2vKey)
        self.dct_path = os.path.join(self.tmp_path, PhyVariables.dctFileKey)

        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)

    # сохранение и зашрузка файлов на комп все в storage
    def get_urls(self):
        urls = []
        if not os.path.isfile(self.urls_path):
            return list()
        with open(self.urls_path, 'r', encoding="utf8") as json_file:
            data_urls = json.load(json_file)
            for url in data_urls:
                urls.append(dict(url=url.get('url'), language=url.get('language', '')))
        return urls

    def get_urls_status(self):
        urls = []
        if not os.path.isfile(self.urls_status_path):
            return list()
        with open(self.urls_status_path, 'r', encoding="utf8") as json_file:
            data_urls = json.load(json_file)
            for url in data_urls:
                urls.append(dict(url=url.get('url'), status=url.get('status', '')))
        return urls

    def get_new_urls(self):
        db_urls = [x.get('url') for x in self.get_urls()]
        old_urls = [x.get('url') for x in self.get_urls_status()]
        sbuf = set(old_urls)
        new_urls = [x for x in db_urls if x not in sbuf]
        return new_urls

    # работает как ДОЗАПИСЬ поэтому вполне логично остаить конкатенацию тут,
    # артикл фетчер просто передает новораспарсеный список
    def save_urls_status(self, urls_status_new):
        urls_status_old = []
        if os.path.isfile(self.urls_status_path):
            urls_status_old = self.get_urls_status()
        urls_status = urls_status_old + urls_status_new
        with open(self.urls_status_path, 'w', encoding="utf8") as file:
            s = json.dumps(urls_status, indent=2, ensure_ascii=False)
            file.write(s)

    # работает как ДОЗАПИСЬ поэтому вполне логично остаить конкатенацию тут,
    # артикл фетчер просто передает новые распарсенные articles_new
    def save_articles(self, articles_new):
        articles_old = []
        if os.path.isfile(self.articles_path):
            articles_old = self.get_articles()
        articles = articles_old + articles_new
        with open(self.articles_path, 'w', encoding="utf8") as file:
            s = json.dumps(articles, indent=2, ensure_ascii=False)
            file.write(s)

    def get_articles(self):
        saved_articles = list()
        with open(self.articles_path, 'r', encoding='utf8') as file:
            data_articles = json.load(file)
            for article in data_articles:
                saved_articles.append(article)
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