import pymongo
from pymongo import MongoClient

from Models.PhygeArticle import BaseArticle, PhyWebArticle, PhyPdfArticle


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
    def add_document(cls, doc: BaseArticle, uuid):
        cls.articles.insert_one({**doc.serialize(),
                                 '_id': uuid,
                                 'serial_id': cls.get_next_number_in_sequence(cls.article_serial_id_sequence_key)})


    @classmethod
    def get_all_documents(cls, filter_fields=None) -> [BaseArticle]:
        filter_fields = filter_fields if filter_fields else dict()
        articles = cls.articles.find(filter_fields).sort('serial_id', pymongo.ASCENDING)
        return [BaseArticle(obj) for obj in articles]

    @classmethod
    def get_all_web_articles(cls, filter_fields=None) -> [PhyWebArticle]:
        web_article_filter = {'type': 'web_article'}
        filter_fields = dict(**filter_fields, **web_article_filter) if filter_fields else web_article_filter
        articles = cls.articles.find(filter_fields).sort('serial_id', pymongo.ASCENDING)
        return [PhyWebArticle(obj) for obj in articles]

    @classmethod
    def get_all_pdf_articles(cls, filter_fields=None) -> [PhyPdfArticle]:
        pdf_article_filter = {'type': 'pdf_article'}
        filter_fields = dict(**filter_fields, **pdf_article_filter) if filter_fields else pdf_article_filter
        articles = cls.articles.find(filter_fields).sort('serial_id', pymongo.ASCENDING)
        return [PhyPdfArticle(obj) for obj in articles]

    @classmethod
    def get_article(cls, uuid) -> dict:
        return cls.articles.find_one({'_id': str(uuid)})
