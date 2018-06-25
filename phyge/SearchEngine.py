from TestCase import TestCase
from Storage import Storage
from PhygeVariables import PhyVariables
from TematicModels import LDAmodel, LSImodel, W2Vmodel


# query will be taken from interface but now we take it from storage
class SearchEngine:
    def __init__(self, test_case_id):
        #self.test_case = TestCase(test_case_id)
        #self.query = query
        #self.new_urls = None
        self.test_case_id = test_case_id
        self.storage = Storage(test_case_id)
        self.lda_model = LDAmodel(self.storage)
        self.lsi_model = LSImodel(self.storage)
        self.w2v_model = W2Vmodel(self.storage)

    def get_model(self):  # инициализируем модель
        self.lsi_model = LSImodel(self.storage)
        self.lda_model = LDAmodel(self.storage)
        self.w2v_model = W2Vmodel(self.storage)

    def find_loaded_model(self, model_name):
        #self.get_model()
        if model_name == 'lsi':
            return self.lsi_model.base_model
        elif model_name == 'lda':
            return self.lda_model.base_model
        elif model_name == 'w2v':
            return self.w2v_model.base_model
        else:
            print("\nWrong model name\n")
            return None

    def train_unloaded_models(self):
        #self.get_model()
        if not self.lsi_model.base_model:
            self.lsi_model.train_models()
        if not self.lda_model.base_model:
            self.lda_model.train_models()
        if not self.w2v_model.base_model:
            self.w2v_model.train_models()

    def get_result(self):  # возвращает результат
        self.test_case = TestCase(self.test_case_id)
        self.test_case.load_by_urls()
        self.train_unloaded_models()
        return self.lda_model.main_test_write(), self.lsi_model.main_test_write(), self.w2v_model.main_test_write()


if __name__ == '__main__':
    test_case_id = PhyVariables.currentTestKey
    search = SearchEngine(test_case_id)
    if search.find_loaded_model('lsi'):
        print("\nStart server\n")
    else:
        print("\nCan't start server, model didn't loaded\n")
        search.train_unloaded_models()
    search.get_result()
