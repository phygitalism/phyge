import time
import abc

from gensim import models
from gensim import similarities

from TrainingSample import TrainingSample


class BaseModel(object):
    TOPIC_NUMBER = 300

    __metaclass__ = abc.ABCMeta

    def __init__(self, training_sample: TrainingSample, model_name='model'):
        self.name = model_name
        self.training_sample = training_sample
        self.dictionary = training_sample.dictionary
        self.corpus = training_sample.corpus

        self.model = self.train_model()

    @abc.abstractmethod
    def train_model(self):
        """Train model."""
        return

    def perform_search(self, normalized_query: [str]):
        index = similarities.MatrixSimilarity(self.model[self.corpus])
        query_vec = self.query_to_vec(normalized_query)
        query_lsi = self.model[query_vec]
        sims = index[query_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])

        return sims

    def query_to_vec(self, normalized_query: [str]):
        return self.dictionary.doc2bow(normalized_query)


class LsiModel(BaseModel):
    def __init__(self, training_sample: TrainingSample):
        BaseModel.__init__(self, training_sample=training_sample, model_name='lsi')

    def train_model(self):
        print('\nLSI model: Обучаем модель...')
        start_time = time.time()
        lsi = models.LsiModel(self.corpus, id2word=self.dictionary, num_topics=self.TOPIC_NUMBER)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return lsi


class LdaModel(BaseModel):
    def __init__(self, training_sample: TrainingSample):
        BaseModel.__init__(self, training_sample=training_sample, model_name='lda')

    def train_model(self):
        print('\nLDA model: Обучаем модель...')
        start_time = time.time()
        lda = models.ldamodel.LdaModel(self.corpus, id2word=self.dictionary, num_topics=self.TOPIC_NUMBER,
                                       passes=20)  # ,iterations=50)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return lda


if __name__ == '__main__':
    testing_sample = TrainingSample()

    lsi = LsiModel(testing_sample)
    lda = LdaModel(testing_sample)
