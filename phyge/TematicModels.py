import time
from pprint import pprint
from gensim import models, similarities
import json
import os

from Storage import Storage
from PhygeVariables import PhyVariables
from TextNormalizer import TextNormalizer
from TestCase import TestCase


class BaseModel:
    TOPIC_NUMBER = 300

    def __init__(self, storage: Storage, model_name='model', path=None):
        self.storage = storage
        self.dct = self.storage.get_dct()
        self.corpus = storage.get_corpus().copy()
        #corpora.MmCorpus.serialize(self.storage.tmp_path + '/deerwester.mm', self.corpus)
        self.base_model = storage.get_model(model_name, path)
        self.model_name = model_name
        self.path = path
        #self.load_func = load_func
        self.train_models()

    # нормализуем запрос
    def query_to_vec(self, query_text):
        query_normalize = TextNormalizer.normalize(query_text)
        dct = self.storage.get_dct()
        return dct.doc2bow(query_normalize)

    def train_models(self):
        if self.base_model is None:
            self.base_model = self.train_model()
            self.storage.save_model(self.base_model, self.path)
            print('Model %s saved ' % self.model_name)

    def find_article(self, query_text, amount=5):
        return self.perform_search(self.base_model[self.corpus], self.base_model[query_text], amount)

    def perform_search(self, corpus_model, query_vec, amount):
        start_time = time.time()
        index = similarities.MatrixSimilarity(corpus_model)
        sims = index[query_vec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        answer_time = round((time.time() - start_time), 3)
        articles = self.storage.get_articles()
        found_articles = []
        for i, similarity in sims[:amount]:
            article_similarity = articles[i].copy()
            article_similarity.update({'id': i,
                                       'similarity': round(float(similarity), 3)})
            article_similarity['text'] = (articles[i]['text'][:200]).replace("', '", '').replace("['", '') + '...'
            article_similarity.pop('normalized_words')
            found_articles.append(article_similarity)
        return answer_time, self.model_name, found_articles

    def show_result_info(self, amount=3):
        answers = []
        for query in self.storage.get_queries():
            query_text = query['text']
            query_vec = self.query_to_vec(query_text)
            answer_time, model_name, answer_articles = self.find_article(query_vec, amount=amount)
            answers.append({'answer_time': answer_time,
                            'model_name': model_name,
                            'answer_articles': answer_articles})
        return answers

    #  функция чтобы посмотреть результат, потом ее не будет
    def main_test_write(self, amount=3):
        query_num = 1
        if not os.path.exists('answers'):
            os.makedirs('answers')
        for m in self.show_result_info(amount):
            print('%s answer time for %s' % (m["answer_time"], m["model_name"]))
            with open('answers/answer.' + m["model_name"] + str(query_num) + ".json", 'w', encoding="utf8") as file:
                query_num += 1
                s = json.dumps(m["answer_articles"], indent=2, ensure_ascii=False)
                file.write(s)

    def load_query_to_vec(self, query_text):
        query_normalize = TextNormalizer.normalize(query_text)
        return self.dct.doc2bow(query_normalize)


class LSImodel(BaseModel):
    def __init__(self, storage: Storage):
        BaseModel.__init__(self, storage=storage, model_name='lsi', path=storage.lsi_path)

    def train_model(self):
        print('\nLSI model: Обучаем модель...')
        start_time = time.time()
        lsi = models.LsiModel(self.corpus, id2word=self.dct, num_topics=self.TOPIC_NUMBER)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return lsi


class LDAmodel(BaseModel):
    def __init__(self, storage: Storage):
        BaseModel.__init__(self, storage=storage, model_name='lda', path=storage.lda_path)

    def train_model(self):
        print('\nLDA model: Обучаем модель...')
        start_time = time.time()
        lda = models.ldamodel.LdaModel(self.corpus, id2word=self.dct, num_topics=self.TOPIC_NUMBER,
                                       passes=20)  # ,iterations=50)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return lda


class W2Vmodel(BaseModel):
    def __init__(self, storage: Storage):
        BaseModel.__init__(self, storage=storage, model_name='w2v', path=storage.w2v_path)

    def find_article(self, query_text, amount=5):
        return super().perform_search(self.corpus, query_text, amount)

    def train_model(self):
        print('\nWord2vec model: Обучаем модель...')
        start_time = time.time()
        documents = self.storage.get_words_list()
        w2v = models.Word2Vec(documents, min_count=5)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return w2v


if __name__ == '__main__':
    test_case_id = PhyVariables.currentTestKey
    test_case = TestCase(test_case_id)
    test_case.setup()
    lsi = LSImodel(test_case.storage)
    lda = LDAmodel(test_case.storage)
    w2v = W2Vmodel(test_case.storage)
    lsi.main_test_write()
    lda.main_test_write()
    w2v.main_test_write()