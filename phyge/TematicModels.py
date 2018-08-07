import time
import abc
import os
from gensim import models, similarities

from Models.TrainingSample import TrainingSample


class BaseModel(object):
    TOPIC_NUMBER = 300
    SHARD_SIZE = 500

    @classmethod
    def trained(cls, name, model, corpus, dictionary, training_sample: TrainingSample):
        instance = cls(name)

        instance.model = model
        instance.corpus = corpus
        instance.dictionary = dictionary

        instance.training_sample = training_sample

        return instance

    def __init__(self, name, model_type):
        self.name = name
        self.type = model_type

        self.model = None
        self.training_sample = None
        self.dictionary = None
        self.corpus = None

    @abc.abstractmethod
    def train_model(self, training_sample: TrainingSample):
        """Train model."""

    def perform_search(self, normalized_query: [str]):
        # index = similarities.MatrixSimilarity(self.model[self.corpus])
        index = similarities.Similarity(output_prefix=os.path.join('out', self.type, 'index_shard'),
                                        corpus=self.model[self.corpus],
                                        shardsize=self.SHARD_SIZE,
                                        num_features=self.dictionary.num_pos)

        query_vec = self.query_to_vec(normalized_query)
        query = self.model[query_vec]
        sims = index[query]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])

        return sims

    def query_to_vec(self, normalized_query: [str]):
        return self.dictionary.doc2bow(normalized_query)


class LsiModel(BaseModel):
    def __init__(self, model_name: str):
        BaseModel.__init__(self, name=model_name, model_type='lsi')

    def train_model(self, training_sample: TrainingSample):
        self.training_sample = training_sample
        self.dictionary = training_sample.dictionary
        self.corpus = training_sample.corpus

        print('\nLSI model: Обучаем модель...')
        start_time = time.time()
        self.model = models.LsiModel(self.corpus, id2word=self.dictionary, num_topics=self.TOPIC_NUMBER)
        print('Learning time:', round((time.time() - start_time), 3), 's')


class LdaModel(BaseModel):
    def __init__(self, model_name: str):
        BaseModel.__init__(self, name=model_name, model_type='lda')

    def train_model(self, training_sample: TrainingSample):
        self.training_sample = training_sample
        self.dictionary = training_sample.dictionary
        self.corpus = training_sample.corpus

        print('\nLDA model: Обучаем модель...')
        start_time = time.time()
        self.model = models.ldamodel.LdaModel(self.corpus, id2word=self.dictionary, num_topics=self.TOPIC_NUMBER,
                                              passes=20)
        print('Learning time:', round((time.time() - start_time), 3), 's')


if __name__ == '__main__':
    pass
