import uuid
import json
import os

from DBController import DBController
from ArticleFetcher import ArticleFetcher


class DatabaseSeeder:

    @classmethod
    def seed(cls):
        DBController.first_setup()

        data_path = 'Resources/ru_slack_urls_clear.json'

        if not os.path.isfile(data_path):
            return list()

        with open(data_path, 'r', encoding='utf8') as data_file:

            data = json.load(data_file)

            article_fetcher = ArticleFetcher()

            for index, article_data in enumerate(data):
                url = article_data['url']
                print(f'download {index+1} of the {len(data)}: {url}')
                article = article_fetcher.download_article(url)

                if article is not None:
                    DBController.add_article(article, str(uuid.uuid4()))
