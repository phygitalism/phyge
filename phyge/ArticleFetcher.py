from Models.PhygeArticle import PhyArticle
from newspaper import Article


class ArticleFetcher:
    def __init__(self, urls):
        self.urls = urls
        self.articles = list()
        self.flag = False

    def fetch(self):
        length = len(self.urls)
        for number, current_url in enumerate(self.urls, start=1):
            #print(str.format('Downloading article {0} from {1} {2}', number, length, current_url))
            #current_url = current_url.replace('habrahabr.ru', 'habr.com')
            print(str.format('Downloading article {0} from {1} {2}', number, length, current_url))
            article_html = Article(url=current_url, language='ru')
            article_html.download()
            if len(article_html.html) > 0:
                # article_html = request(url=current_url, method='GET').text
                article = PhyArticle()
                article.transform(article_html, current_url)
                if len(article.normalized_words) > 0:
                    self.articles.append(article)
                    self.flag = True
                else:
                    print('NO FOUND words in the article', number, 'url:', current_url)
            else:
                print('article', number, 'doesn\'t parsed! Url:', current_url)
        return self.articles
