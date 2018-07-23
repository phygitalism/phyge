import uuid
import json
import os

from DBController import DBController
from ArticleFetcher import ArticleFetcher


class DatabaseSeeder:

    @classmethod
    def seed(cls):
        DBController.first_setup()

        data_path = 'Resources/ru_slack_short_urls_list.json'

        if not os.path.isfile(data_path):
            return list()

        with open(data_path, 'r', encoding='utf8') as data_file:

            data = json.load(data_file)

            article_fetcher = ArticleFetcher()

            for article_data in data:
                url = article_data['url']
                article = article_fetcher.download_article(url)

                if article is not None:
                    DBController.add_article(article, str(uuid.uuid4()))
