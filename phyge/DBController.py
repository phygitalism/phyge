import pymongo
from pymongo import MongoClient

from Models.PhygeArticle import PhyArticle


class DBController:

    mongo_client = MongoClient('mongo-db', 27017)
    db = mongo_client.phydge
    articles = db.articles
    counters = db.counters

    article_serial_id_sequence_key = 'article_serial_id'

    @classmethod
    def first_setup(cls):
        cls.counters.insert_one({'_id': cls.article_serial_id_sequence_key,
                                 'seq': 0})

    @classmethod
    def get_next_number_in_sequence(cls, name: str):
        number = cls.counters.find_one_and_update({'_id': name}, {'$inc': {'seq': 1}},
                                                  upsert=True, return_document=pymongo.ReturnDocument.AFTER)
        return number['seq']

    @classmethod
    def add_article(cls, article: PhyArticle, uuid):
        cls.articles.insert_one({
            '_id': str(uuid),
            'serial_id': cls.get_next_number_in_sequence(cls.article_serial_id_sequence_key),
            'title': article.title,
            'source': article.source
        })

    @classmethod
    def get_all_articles(cls, filter_fields=None) -> [dict]:
        filter_fields = filter_fields or {}
        return [x for x in cls.articles.find(filter_fields).sort('serial_id', pymongo.ASCENDING)]

    @classmethod
    def get_article(cls, uuid) -> dict:
        return cls.articles.find_one({'_id': str(uuid)})
