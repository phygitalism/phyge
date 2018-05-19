import time
from pprint import pprint
from gensim import corpora, models, similarities
from Models.PhygeArticle import PhyArticle
from Storage import Storage
from Models.Query import Query


# import sys, os # Для записи в файл


class TematicModels:
    TOPIC_NUMBER = 200

    def __init__(self, TEST_NUMBER=1):
        self.TEST_NUMBER = TEST_NUMBER
        self.corpus = self.__load_corpus()
        self.lsi = self.load_LSI_model()
        self.lda = self.load_LDA_model()

    def find_article(self, query_text, model='lsi', amount=5):
        if model == 'lsi':
            return self.__perform_search(self.lsi[self.corpus], self.lsi[query_text], amount)
        elif model == 'lda':
            return self.__perform_search(self.lda[self.corpus], self.lda[query_text], amount)

    def __perform_search(self, corpus_model, query_vec, amount):
        start_time = time.time()
        index = similarities.MatrixSimilarity(corpus_model)
        sims = index[query_vec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        print('answer', sims[0:amount])
        print('answer time:', round((time.time() - start_time), 3), 's')
        articles: [PhyArticle] = self.test_case.articles
        found_articles = []
        for index, similarity in sims[0:amount]:
            article_similarity = {'id': index,
                                  'title': articles[index].title,
                                  'url': articles[index].downloaded_from_url,
                                  'text': (articles[index].text[0:200]).replace("', '", '') + '...',
                                  'similarity': round(float(similarity), 3)}
            found_articles.append(article_similarity)
        return found_articles

    def load_query_to_vec(self, query_text):
        query = Query({'text': query_text})
        query_normalize = query.normalized_words
        return self.dct.doc2bow(query_normalize)

    def __load_corpus(self):
        storage = Storage()
        self.test_case = storage.load_test_case(self.TEST_NUMBER)
        self.test_case.setup()
        df = self.test_case.values
        documents = []
        for columns in df.columns:
            documents.append(df[columns].dropna().tolist())
        self.dct = corpora.Dictionary(documents)
        return [self.dct.doc2bow(doc) for doc in documents]

    def load_LSI_model(self):
        print('\nLSI model loadind...')
        lsi_path = self.test_case.path + '/tmp/' + 'phydge.lsi'
        try:
            lsi = models.lsimodel.LsiModel.load(lsi_path)
            print('Loaded')
        except:
            print('LSI model: Модель не найдена')
            start_time_LSI = time.time()
            lsi = models.LsiModel(self.corpus, id2word=self.dct, num_topics=self.TOPIC_NUMBER)
            print('Learning time:', round((time.time() - start_time_LSI), 3), 's')
            lsi.save(lsi_path)
        return lsi

    def load_LDA_model(self):
        print('LDA model loading...')
        lda_path = self.test_case.path + '/tmp/' + 'phydge.lda'
        try:
            lda = models.ldamodel.LdaModel.load(lda_path)
            print('Loaded')
        except:
            print('LDA model: Модель не найдена')
            start_time_LDA = time.time()
            lda = models.ldamodel.LdaModel(self.corpus, id2word=self.dct, num_topics=self.TOPIC_NUMBER, passes=20)
            print('Learning time:', round((time.time() - start_time_LDA), 3), 's')
            lda.save(lda_path)
        return lda


if __name__ == '__main__':
    search_articles = {'text': ' Текст из поискового запроса',
                       'amount': 2}
    query_text = search_articles['text']
    amount = search_articles['amount']

    tematic_models = TematicModels(TEST_NUMBER=3)
    query_text = tematic_models.test_case.queries[0].text
    print('TRUE TITLE', tematic_models.test_case.queries[0].title)
    query_vec = tematic_models.load_query_to_vec(query_text)

    lsi_answer = tematic_models.find_article(query_vec, model='lsi', amount=amount)
    pprint(lsi_answer)

    lda_answer = tematic_models.find_article(query_vec, model='lda', amount=amount)
    pprint(lda_answer)
    print('------------------------------------\n')
    # dct.save(path + '/deerwester.dict')
    # corpora.MmCorpus.serialize(path + '/deerwester.mm', corpus)  # store to disk, for later use
