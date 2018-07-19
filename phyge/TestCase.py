from enum import Enum
import re
from ArticleFetcher import ArticleFetcher
from Storage import Storage
from TextNormalizer import TextNormalizer
from Models.PhygeArticle import PhyArticle


class DownloadArticlesState(Enum):
    OldArticle, NewArticle = range(2)

    def __str__(self):
        return str(self.name)


class TestCase:
    def __init__(self, test_case_id):
        self.storage = Storage(test_case_id)
        self.article_fetcher = ArticleFetcher()
        self.id = self.storage.test_case_id
        self.path = self.storage.test_case_path
        self.path_tmp = self.storage.tmp_path
        self.queries = self.storage.get_queries()
        self.articles = self.storage.get_articles()
        self.values = self.storage.get_words_df_json()
        self.fetch_state = DownloadArticlesState.OldArticle

        self.db = self.storage.get_db()

    def setup(self):
        existing_data = [article.source for article in self.articles]
        filtred_data = [x for x in self.db if x['source'] not in existing_data]
        data_number = len(filtred_data)
        if data_number > 0:
            for i, current_data in enumerate(filtred_data, start=1):
                print(str.format('Downloading article {0} from {1} {2}', i, data_number, current_data['source']))
                if current_data["data_type"] == "web_article":
                    current_article = self.article_fetcher.load_article(current_data)
                elif current_data["data_type"] == "note":
                    current_article = self.load_note_article(current_data)
                else:
                    print("Key error in data base\n")
                    current_article = None
                if current_article:
                    self.articles.append(current_article)
                else:
                    print("Error while download article", i)
        self.storage.save_articles(self.articles)
        self.values = self.storage.get_words_list()

    def load_note_article(self, current_data):
        text = current_data['text']
        text = re.sub(r'\{[^*]*\}', '', text)
        normalized_words = TextNormalizer.normalize(text)
        return PhyArticle({'source': current_data['source'],
                           'title': current_data['title'],
                           'text': text,
                           'language': current_data['language'],
                           'normalized_words': normalized_words})
