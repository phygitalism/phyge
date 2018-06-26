from TestCase import TestCase
from TematicModels import LDAmodel, LSImodel, W2Vmodel
from Storage import Storage
from PhygeVariables import PhyVariables
from TextNormalizer import TextNormalizer

from gensim import similarities
import time
import json
import os
from enum import Enum


class ServerState(Enum):
    Start, Stop = range(2)

    def __str__(self):
        return str(self.name)


# query will be taken from interface but now we take it from storage
class SearchEngine:
    def __init__(self, query, model_name, test_case_id):
        #self.test_case = TestCase(test_case_id)
        #self.new_urls = None
        self.query = query
        self.model_name = model_name
        self.test_case_id = test_case_id
        self.storage = Storage(test_case_id)
        self.model = None
        self.base_model = None
        try:
            self.base_model = self.get_model()
        except Exception as error:
            print('Error' + repr(error))
        if self.base_model:
            self.server_state = ServerState.Start
        else:
            self.server_state = ServerState.Stop

    def get_model(self):  # инициализируем модель
        if self.model_name == 'lsi':
            self.model = LSImodel(self.storage)
        elif self.model_name == 'lda':
            self.model = LDAmodel(self.storage)
        elif self.model_name == 'w2v':
            self.model = W2Vmodel(self.storage)
        else:
            raise Exception('Wrong model name!')
        return self.model.base_model

    def train_model(self):
        if not self.base_model:
            self.model.train_models()

    # так как докачка будет происходить отдельно эта функция временная
    def get_result(self):  # возвращает результат
        self.test_case = TestCase(self.test_case_id)
        self.test_case.setup()
        # self.train_model()
        return self.write_answers()

    # нормализуем запрос
    def query_to_vec(self, query_text):
        query_normalize = TextNormalizer.normalize(query_text)
        dct = self.storage.get_dct()
        return dct.doc2bow(query_normalize)

    def find_article(self, query_text, amount=5):
        if self.model_name == 'w2v':
            return self.perform_search(self.model.corpus, query_text, amount)
        return self.perform_search(self.base_model[self.model.corpus], self.base_model[query_text], amount)

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

    def queries_result(self, amount=3):
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
    def write_answers(self, amount=3):
        query_num = 1
        path = os.path.join(self.storage.tmp_path, 'answers')
        if not os.path.exists(path):
            os.makedirs(path)
        for answer_info in self.queries_result(amount):
            print('%s answer time for %s' % (answer_info["answer_time"], answer_info["model_name"]))
            file_name = 'answer.' + answer_info["model_name"] + str(query_num) + ".json"
            with open(os.path.join(path, file_name), 'w', encoding="utf8") as file:
                query_num += 1
                s = json.dumps(dict(model_name=self.model_name,
                                    answers=answer_info["answer_articles"]), indent=2, ensure_ascii=False)
                file.write(s)


if __name__ == '__main__':
    test_case_id = PhyVariables.currentTestKey
    search = SearchEngine(query=None, test_case_id=test_case_id, model_name='w2v')
    if search.server_state == ServerState.Stop:
        print("\nCan't start server, model didn't loaded\n")
        search.train_model()
    else:
        print("\nStart server\n")
        search.get_result()
