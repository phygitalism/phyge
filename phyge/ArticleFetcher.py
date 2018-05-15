from Models.PhygeArticle import PhyArticle
from newspaper import Article


class ArticleFetcher:
    def __init__(self, urls):
        self.urls = urls
        self.articles = list()

    def fetch(self):
        for number, current_url in enumerate(self.urls, start=1):
            print(str.format('Downloading article {0} from {1} {2}', number, len(self.urls), current_url))
            article_html = Article(url=current_url, language='ru')
            article_html.download()
            if len(article_html.html) > 0:
                # article_html = request(url=current_url, method='GET').text
                article = PhyArticle()
                article.transform(article_html, current_url)
                if len(article.normalized_words) > 0:
                    self.articles.append(article)
                else:
                    print('NO FOUND words in the article', number, 'url:', current_url)
            else:
                print('article', number, 'doesn\'t parsed! Url:', current_url)
        return self.articles
