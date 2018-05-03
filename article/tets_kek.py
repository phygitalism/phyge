import pandas as pd

from ArticleFetcher import ArticleFetcher
from ArticleSerializer import ArticleSerializer


def filtred_download_urls(urls_to_download, existing_urls):
    return [x for x in urls_to_download if x not in existing_urls]


if __name__ == '__main__':
    data_url = pd.read_csv('url_test.csv')
    urls_to_download = data_url.iloc[0:3, 0]
    saved_articles = ArticleSerializer.deserialize()
    existing_urls = [article.downloaded_from_url for article in saved_articles]

    filtred_urls = filtred_download_urls(urls_to_download, existing_urls)
    print('New url:\n', filtred_urls)

    article_fetcher = ArticleFetcher(filtred_urls)
    downloaded_articles = article_fetcher.fetch()

    downloaded_articles += saved_articles
    article_serializer = ArticleSerializer.serialize(downloaded_articles)
    desirialized_articles = ArticleSerializer.deserialize()

    print('\nTitle parsed article and url:')
    for i in range(0, len(desirialized_articles)):
        print(desirialized_articles[i], desirialized_articles[i].downloaded_from_url)
