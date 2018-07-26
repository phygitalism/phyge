import uuid
import json
import os

from DBController import DBController
from ArticleFetcher import ArticleFetcher
from Models.PhygeArticle import PhyPdfArticle
from TextNormalizer import TextNormalizer


class DatabaseSeeder:

    @classmethod
    def seed(cls):
        DBController.first_setup()
        cls.__seed_web_articles()
        cls.__seed_pdf_articles()

    @classmethod
    def __seed_web_articles(cls):
        data_path = 'Resources/ru_slack_short_urls_list.json'

        if not os.path.isfile(data_path):
            print('Resource does not exist!')
            return

        with open(data_path, 'r', encoding='utf8') as data_file:

            data = json.load(data_file)

            article_fetcher = ArticleFetcher()

            for index, article_data in enumerate(data):
                url = article_data['url']
                print(f'download {index+1} of the {len(data)}: {url}')
                article = article_fetcher.download_article(url)

                if article is not None:
                    DBController.add_document(article, str(uuid.uuid4()))

    @classmethod
    def __seed_pdf_articles(cls):
        data_path = 'Resources/pdf_articles_short.json'

        if not os.path.isfile(data_path):
            print('Resource does not exist!')
            return

        with open(data_path, 'r', encoding='utf8') as data_file:

            data = json.load(data_file)

            for index, article_data in enumerate(data):
                title = article_data['title']
                text = article_data['text']
                normalized_words = TextNormalizer.normalize(text)
                article = PhyPdfArticle({**article_data,
                                         'lang': 'en',
                                         'normalized_words': normalized_words})

                print(f'add {index+1} of the {len(data)} articles: {title}')

                if article is not None:
                    DBController.add_document(article, str(uuid.uuid4()))
