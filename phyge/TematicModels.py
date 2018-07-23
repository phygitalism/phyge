import time
from gensim import models
from gensim.matutils import hellinger, cossim, jaccard
from gensim import similarities
from TrainingSample import TrainingSample

import abc


class BaseModel(object):
    TOPIC_NUMBER = 300

    __metaclass__ = abc.ABCMeta

    def __init__(self, training_sample: TrainingSample, model_name='model'):
        self.model_name = model_name
        self.training_sample = training_sample
        self.dictionary = training_sample.dictionary
        self.corpus = training_sample.corpus

        self.model = self.train_model()

    @abc.abstractmethod
    def perform_search(self, normalized_query: [str]):
        """Perform search."""
        return

    @abc.abstractmethod
    def train_model(self):
        """Train model."""
        return

    def query_to_vec(self, normalized_query: [str]):
        return self.dictionary.doc2bow(normalized_query)


class LSImodel(BaseModel):
    def __init__(self, training_sample: TrainingSample):
        BaseModel.__init__(self, training_sample=training_sample, model_name='lsi')

    def train_model(self):
        print('\nLSI model: Обучаем модель...')
        start_time = time.time()
        lsi = models.LsiModel(self.corpus, id2word=self.dictionary, num_topics=self.TOPIC_NUMBER)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return lsi

    def perform_search(self, normalized_query: [str]):
        start_time = time.time()
        index = similarities.MatrixSimilarity(self.model[self.corpus])
        query_vec = self.query_to_vec(normalized_query)
        query_lsi = self.model[query_vec]
        sims = index[query_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        answer_time = round((time.time() - start_time), 3)

        articles = self.training_sample.articles
        found_articles = []
        amount = 3
        for index, similarity in sims[:amount]:
            answer = {'id': index,
                      'title': articles[index].title,
                      'source': articles[index].source,
                      'text': (articles[index].text[0:200]).replace("', '", '').replace("['", '') + '...',
                      'similarity': round(float(similarity), 3)}
            found_articles.append(answer)
        return answer_time, 'lsi', found_articles


class LDAmodel(BaseModel):
    def __init__(self, training_sample: TrainingSample):
        BaseModel.__init__(self, training_sample=training_sample, model_name='lda')

    def train_model(self):
        print('\nLDA model: Обучаем модель...')
        start_time = time.time()
        lda = models.ldamodel.LdaModel(self.corpus, id2word=self.dictionary, num_topics=self.TOPIC_NUMBER,
                                       passes=20)  # ,iterations=50)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return lda

    def perform_search(self, normalized_query: [str]):
        pass


class W2Vmodel(BaseModel):
    def __init__(self, training_sample: TrainingSample):
        BaseModel.__init__(self, training_sample=training_sample, model_name='w2v')

    def train_model(self):
        print('\nWord2vec model: Обучаем модель...')
        start_time = time.time()
        w2v = models.Word2Vec(self.training_sample.get_documents, min_count=5)
        print('Learning time:', round((time.time() - start_time), 3), 's')
        return w2v

    def perform_search(self, normalized_query: [str]):
        pass


if __name__ == '__main__':
    testing_sample = TrainingSample()

    lsi = LSImodel(testing_sample)
    lda = LDAmodel(testing_sample)
    w2v = W2Vmodel(testing_sample)
