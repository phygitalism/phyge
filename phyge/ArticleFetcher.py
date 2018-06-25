from newspaper import Article
from TextNormalizer import TextNormalizer
from readability.readability import Document
from bs4 import BeautifulSoup

from Models.PhygeTranslate import PhyTranslate

class ArticleFetcher:
    def __init__(self):
        self.urls = None
        self.word_limit = 30
    def load_articles(self, storage, urls_new):
        urls_number = len(urls_new)
        urls_status = []
        articles = list()
        for i, current_url in enumerate(urls_new, start=1):
            current_url_status = {"url": current_url}
            print(str.format('Downloading article {0} from {1} {2}', i, urls_number, current_url))
            article_html = self.load_html(current_url)
            if len(article_html) > 0:
                current_article = self.parse_html(current_url, article_html)
                #if len(current_article['normalized_words']) > self.word_limit:
                #    articles.append(current_article)
                #    current_url_status["status"] = "OK"
                if len(current_article['normalized_words']) > 0:
                    articles.append(current_article)
                    current_url_status["status"] = "OK"
                else:
                    current_url_status["status"] = "LOAD_ERR"
            else:
                current_url_status["status"] = "PARSE_ERR"
            urls_status.append(current_url_status)
        storage.save_urls_status(urls_status)
        storage.save_articles(articles)
        return articles

    def load_html(self, current_url):
        article_html = Article(url=current_url, language='ru')
        article_html.download()
        return article_html.html

    # третьим аргументом шел язык
    def parse_html(self, current_url, article_html):
        readable_html = Document(article_html).summary()
        title = Document(article_html).short_title()
        text = self.__transform_to_single_line(readable_html)

        if PhyTranslate.detect_language(text) == 'en':
            text = PhyTranslate.translate(text, title, current_url)

        normalized_words = TextNormalizer.normalize(text)
        return {'url': current_url,
                'title': title,
                'text': text,
                #'language': language,
                'normalized_words': normalized_words}

    def __transform_to_single_line(self, raw_html):
        soup = BeautifulSoup(raw_html, "lxml")
        return str(soup.findAll(text=True)).replace("\\n", "").replace("\\r", "").replace('\\xa0', '').replace('\'', '')
