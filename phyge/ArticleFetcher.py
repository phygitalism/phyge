from newspaper import Article
from TextNormalizer import TextNormalizer
from readability.readability import Document
from bs4 import BeautifulSoup

from Models.PhygeTranslate import PhyTranslate
from Models.PhygeArticle import PhyWebArticle
import re


class ArticleFetcher:
    def __init__(self):
        self.word_limit = 30

    def download_article(self, url: str) -> PhyWebArticle:
        article_html = self.load_html(url)
        if len(article_html) > 0:
            article = self.parse_html(url, article_html)
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

    def parse_html(self, current_url, article_html, language='ru'):
        readable_html = Document(article_html).summary()
        title = Document(article_html).short_title()
        text = self.__transform_to_single_line(readable_html)
        text = re.sub(r'\{[^*]*\}', '', text)

        if language == 'en':
            text = PhyTranslate.translate(text, title, current_url)

        normalized_words = TextNormalizer.normalize(text)
        web_article = PhyWebArticle({
            PhyWebArticle.source_key: current_url,
            PhyWebArticle.title_key: title,
            PhyWebArticle.text_key: text,
            PhyWebArticle.language_key: language,
            PhyWebArticle.normalized_words_key: normalized_words
        })

        return web_article

    @staticmethod
    def __transform_to_single_line(raw_html):
        soup = BeautifulSoup(raw_html, 'lxml')
        result = str(soup.findAll(text=True))\
            .replace("\\n", '')\
            .replace("\\r", '')\
            .replace('\\xa0', '')\
            .replace('\'', '')\
            .replace('\\t', '')

        return result
