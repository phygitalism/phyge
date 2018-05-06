from requests import request
from PhyArticle import PhyArticle
from newspaper import Article


class ArticleFetcher:
    def __init__(self, urls):
        self.urls = urls
        self.articles = list()

    def fetch(self):
        for current_url in self.urls:
            article_html = Article(url=current_url, language='ru')
            article_html.download()
            # article_html = request(url=current_url, method='GET').text
            article = PhyArticle()
            article.transform(article_html, current_url)
            self.articles.append(article)
        return self.articles
