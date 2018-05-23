from readability.readability import Document
from bs4 import BeautifulSoup

from TextNormalizer import TextNormalizer


class PhyArticle:
    def __init__(self, obj=None):
        if obj is None:
            obj = dict()

        self.downloaded_from_url = obj.get('url', '')
        self.title = obj.get('title', '')
        self.readable_html = obj.get('readable_html', '')
        self.text = obj.get('text', '')
        self.normalized_words = obj.get('normalized_words', list())
        self.language = obj.get('language', '')

    def deserialize_from(self, obj: dict):
        return PhyArticle(obj)

    def __str__(self):
        return self.title

    def transform(self, article_html, downloaded_from_url):
        self.downloaded_from_url = downloaded_from_url
        self.readable_html = Document(article_html.html).summary()
        self.title = Document(article_html.html).short_title()
        self.text = self.__transform_to_single_line(self.readable_html)
        if self.language == 'en':
            pass
        self.normalized_words = TextNormalizer.normalize(self.text)

    def __transform_to_single_line(self, raw_html):
        soup = BeautifulSoup(raw_html, "lxml")
        return str(soup.findAll(text=True)).replace("\\n", "").replace("\\r", "").replace('\\xa0', '').replace('\'', '')

    def serialized(self):
        return {'url': self.downloaded_from_url,
                'title': self.title,
                'text': self.text,
                'language': self.language,
                'normalized_words': self.normalized_words}
