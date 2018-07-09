import time
from gensim import models, similarities

from Storage import Storage
from PhygeVariables import PhyVariables
from TestCase import TestCase


class BaseModel:
    TOPIC_NUMBER = 300

    def __init__(self, storage: Storage, model_name='model', path=None):
        self.storage = storage
        self.dct = self.storage.get_dct_for_model()
        self.corpus = storage.get_corpus().copy()
        #corpora.MmCorpus.serialize(self.storage.tmp_path + '/deerwester.mm', self.corpus)
        self.base_model = storage.get_model(model_name, path)
        self.model_name = model_name
        self.path = path

    def train_models(self):
        if self.base_model is None:
            self.base_model = self.train_model()
            self.storage.save_model(self.base_model, self.path)
            print('Model %s saved ' % self.model_name)


class LSImodel(BaseModel):
    def __init__(self, storage: Storage):
        BaseModel.__init__(self, storage=storage, model_name='lsi', path=storage.lsi_path)

    def train_model(self):
        print('\nLSI model: Обучаем модель...')
        start_time = time.time()
        print(self.corpus)
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
    lsi.train_models()
    lda.train_models()
    w2v.train_models()