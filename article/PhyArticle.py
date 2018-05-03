from readability.readability import Document
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
import pymorphy2
import pandas as pd


class PhyArticle:
    def __init__(self, obj=None):
        if obj is None:
            obj = dict()

        self.downloaded_from_url = obj.get('url', '')
        self.title = obj.get('title', '')
        self.normalized_words = obj.get('normalized_words', list())
        self.readable_html = obj.get('readable_html', '')
        self.text = obj.get('text', '')

    def deserialize_from(self, obj: dict):
        return PhyArticle(obj)

    def __str__(self):
        return self.title

    def transform(self, html, downloaded_from_url):
        self.downloaded_from_url = downloaded_from_url
        self.readable_html = Document(html).summary()
        self.title = Document(html).short_title()
        self.text = self.__transform_to_single_line(self.readable_html)
        self.normalized_words = self.__fetch_words()

    def __transform_to_single_line(self, raw_html):
        soup = BeautifulSoup(raw_html, "lxml")
        return str(soup.findAll(text=True)).replace("\\n", "").replace("\\r", "")

    def __tokenize_text(self, text):
        tokens = re.sub('[^\w]', ' ', text).split()
        return list(map(str.lower, tokens))

    def __normalize_tokens(self, tokens):
        morph = pymorphy2.MorphAnalyzer()
        return list(map(lambda x: morph.parse(x)[0].normal_form, tokens))

    def __fetch_words(self):
        text_tokens = self.__tokenize_text(self.text)
        russian_words = re.compile('[А-Яа-я]+').findall(' '.join(text_tokens))
        filtered_tokens = list(filter(lambda x: x not in stopwords.words('russian') and len(x) > 1, russian_words))
        return self.__normalize_tokens(filtered_tokens)

    def serialized(self):
        return {'url': self.downloaded_from_url,
                'title': self.title,
                'normalized_words': self.normalized_words}