from ArticleFetcher import ArticleFetcher
from Storage import Storage


class TestCase:
    def __init__(self, test_case_id):
        self.storage = Storage(test_case_id)
        self.parser = ArticleFetcher()
        self.new_urls = None
        # то что ниже можно убрать
        self.articles = None
        self.id = self.storage.test_case_id
        self.path = self.storage.test_case_path  # нужен только в usi можно убрать
        self.urls = self.storage.get_urls()
        self.queries = self.storage.get_queries()
        self.values = self.storage.get_words_list()

    def check_if_new_urls(self):  # проверяет есть ли новые ссылки
        self.new_urls = self.storage.get_new_urls()
        if self.new_urls:
            return True
        return False

    def load_by_urls(self):  # загрузка текстов по новым ссылкам
        if self.check_if_new_urls():
            self.parser.load_articles(self.storage, self.new_urls)
        self.articles = self.storage.get_articles()

    def setup(self):
        self.load_by_urls()

    #def uci_representation(self, path):
    #    pairs = zip(range(len(self.articles)), self.articles)
    #    data = dict((key, value.normalized_words) for key, value in pairs)
    #    bag_of_words = BagOfWordsModel(data)
    #    bag_of_words.to_uci(model_name='articles', save_folder=path + '/uci')
