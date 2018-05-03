from readability.readability import Document
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
import pymorphy2


class PhyArticle:
    def __init__(self, obj=None):
        if obj is None:
            obj = dict()

        self.downloaded_from_url = obj.get('url', '')
        self.title = obj.get('title', '')
        self.readable_html = obj.get('readable_html', '')
        self.text = obj.get('text', '')
        self.normalized_words = obj.get('normalized_words', list())

    def deserialize_from(self, obj: dict):
        return PhyArticle(obj)

    def __str__(self):
        return self.title

    def transform(self, article_html, downloaded_from_url):
        self.downloaded_from_url = downloaded_from_url
        self.readable_html = Document(article_html.html).summary()
        self.title = Document(article_html.html).short_title()
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
        russian_words = self.__normalize_tokens(russian_words)
        return list(filter(lambda x: x not in stopwords.words('russian') and len(x) > 1, russian_words))

    def serialized(self):
        return {'url': self.downloaded_from_url,
                'title': self.title,
                'normalized_words': self.normalized_words}