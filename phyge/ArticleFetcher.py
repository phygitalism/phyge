from newspaper import Article
from TextNormalizer import TextNormalizer
from readability.readability import Document
from bs4 import BeautifulSoup

from Models.PhygeTranslate import PhyTranslate
from Models.PhygeArticle import PhyArticle
import re


class ArticleFetcher:
    def __init__(self):
        self.word_limit = 30

    def load_article(self, data_new):
        article_html = self.load_html(data_new['source'])
        if len(article_html) > 0:
            article = self.parse_html(data_new['source'], article_html, data_new['language'])
            if len(article.normalized_words) == 0:
                print('LOAD ERR')
                article = None
        else:
            print('PARSE ERR')
            article = None
        return article

    def load_html(self, current_url):
        article_html = Article(url=current_url, language='ru')
        article_html.download()
        return article_html.html

    def parse_html(self, current_url, article_html, language):
        readable_html = Document(article_html).summary()
        title = Document(article_html).short_title()
        text = self.__transform_to_single_line(readable_html)
        text = re.sub(r'\{[^*]*\}', '', text)
        # if PhyTranslate.detect_language(text) == 'en':
        # if language == 'en':
        text = PhyTranslate.translate(text, title, current_url)
        normalized_words = TextNormalizer.normalize(text)
        return PhyArticle({'source': current_url,
                           'title': title,
                           'text': text,
                           'language': language,
                           'normalized_words': normalized_words})

    def __transform_to_single_line(self, raw_html):
        soup = BeautifulSoup(raw_html, "lxml")
        return str(soup.findAll(text=True)).replace("\\n", "").replace("\\r", "").replace('\\xa0', '').replace('\'',
                                                                                                               '').replace(
            '\\t', '')
