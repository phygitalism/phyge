from TestCase import TestCase
from TematicModels import LDAmodel, LSImodel, W2Vmodel
from Storage import Storage
from PhygeVariables import PhyVariables
from Models.PhygeArticle import PhyArticle
from gensim import similarities
import time
from enum import Enum
from pprint import pprint

## Test
from gensim.matutils import hellinger, cossim, jaccard
from gensim.similarities import WmdSimilarity
##


class ServerState(Enum):
    Start, Stop = range(2)

    def __str__(self):
        return str(self.name)


# query will be taken from interface but now we take it from storage
class SearchEngine:
    def __init__(self, query, model_name, test_case_id):
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

    def query_to_vec(self, query):
        query_normalize = query.normalized_words
        dct = self.storage.get_dct_for_model()
        return dct.doc2bow(query_normalize)

    def find_article(self, query_text, amount=5):
        if self.model_name == 'w2v':
            return self.perform_search(self.model.corpus, query_text, amount)
        return self.perform_search(self.base_model[self.model.corpus], self.base_model[query_text], amount)

    def perform_search(self, corpus_model, query_vec, amount):
        start_time = time.time()
        index = similarities.MatrixSimilarity(corpus_model)

        # Change this to change simularity function
        # sims = [(document, my_sim_fnc(document, query)) for document in index]


        sims = index[query_vec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])

        answer_time = round((time.time() - start_time), 3)
        articles: [PhyArticle] = self.storage.get_articles()
        found_articles = []

        for index, similarity in sims[:amount]:
            article_similarity = {'id': index,
                                  'title': articles[index].title,
                                  'source': articles[index].source,
                                  'text': (articles[index].text[0:200]).replace("', '", '').replace("['", '') + '...',
                                  'similarity': round(float(similarity), 3)}
                                 # 'Hellinger': round(float(hellinger(query_vec, corpus_model[index])), 3),
                                 #  'Cosine similarity': round(cossim(query_vec, corpus_model[index]), 3)}
                                  #,'Jaccard distance(less is better)': round(float(jaccard(query_vec, corpus_model[index])), 3)}
            if self.model_name == 'lda' or 'lsi':
                article_similarity['Hellinger'] = round(float(hellinger(query_vec, corpus_model[index])), 3)
                article_similarity['Jaccard distance(less is better)'] = round(float(jaccard(query_vec, corpus_model[index])), 3)
            elif self.model_name == 'w2v':
                article_similarity['Jaccard distance(less is better)'] = round(float(jaccard(query_vec, corpus_model[index])), 3)
            else:
                continue
            found_articles.append(article_similarity)
        return answer_time, self.model_name, found_articles

    def get_answers(self, amount=3):
        answers = []
        for query in self.query:
            query_vec = self.query_to_vec(query)
            answer_time, model_name, answer_articles = self.find_article(query_vec, amount=amount)
            print('%s answer time for %s' % (answer_time, model_name))
            answers.append({'answer_time': answer_time,
                            'model_name': model_name,
                            'answer_articles': answer_articles,
                            'query': str(query)})
        self.storage.save_answers(answers)
        return answers


if __name__ == '__main__':
    test_case_id = PhyVariables.currentTestKey
    test_case = TestCase(test_case_id)
    test_case.setup()
    storage = Storage(test_case_id)
    queries = storage.get_queries()
    search = SearchEngine(query=queries, test_case_id=test_case_id, model_name='w2v')
    if search.server_state == ServerState.Stop:
        print("\nCan't start server, model didn't loaded\n")
        search.train_model()
    else:
        print("\nStart server\n")
        pprint(search.get_answers(amount=2))
