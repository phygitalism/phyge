from nltk.corpus import stopwords
from ArticleSerializer import ArticleSerializer


def expirements_1():
    # found bug with filter stopwords
    saved_articles = ArticleSerializer.deserialize()
    normalize_words = [article.normalized_words for article in saved_articles]
    normalize_words[1].append('это')
    russian_words = normalize_words[1]
    print(russian_words)
    filtered_tokens = list(filter(lambda x: x not in stopwords.words('russian') and len(x) > 1, russian_words))
    print('FILTER')
    print(filtered_tokens)


def expirements_2():
    # found bug with html request
    current_url = 'https://hightech.fm/2018/04/13/golos'

    from readability.readability import Document
    from newspaper import Article

    article = Article(url=current_url, language='ru')
    article.download()
    kek = Document(article.html).summary()
    # print('kek', article.html)
    with open('kek1-source.html', 'w+', encoding='utf8') as file:
        file.write(article.html)

    from requests import request
    article_html = request(url=current_url, method='GET').text
    kek2 = Document(article_html).summary()
    print('kek 2')
    # print(article_html)
    with open('kek2-source.html', 'w+', encoding='utf8') as file:
        file.write(article_html)

    with open('kek1-summary.html', 'w+', encoding='utf8') as file:
        file.write(kek)

    with open('kek2-summary.html', 'w+', encoding='utf8') as file:
        file.write(kek2)
