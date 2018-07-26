import uuid
import json
import os

from DBController import DBController
from ArticleFetcher import ArticleFetcher
from TextNormalizer import TextNormalizer


class DatabaseSeeder:

    @classmethod
    def seed(cls):
        DBController.first_setup()
        cls.__seed_web_articles()

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

