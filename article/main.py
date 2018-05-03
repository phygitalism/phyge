import pandas as pd
from ArticleFetcher import ArticleFetcher
from ArticleSerializer import ArticleSerializer
from BagOfWordsModel import BagOfWordsModel


def filtred_download_urls(urls_to_download, existing_urls):
    return [x for x in urls_to_download if x not in existing_urls]


def create_df_words(article):
    df_words_in_doc = pd.DataFrame()
    for i in range(0, len(article)):
        df_words_in_doc[i] = pd.Series(article[i].normalized_words)
        df_words_in_doc.to_csv('value.csv', index=False, encoding='utf8')
    print(article[1].title)
    print(article[1].normalized_words)
    return df_words_in_doc


def create_uci(article):
    dict_kek = {}
    for i in range(0, len(article)):
        dict_kek.update({i: str(article[i].normalized_words)})
    bag_of_words = BagOfWordsModel(dict_kek)
    bag_of_words.to_uci()

if __name__ == '__main__':
    data_url = pd.read_csv('url_test.csv')
    urls_to_download = data_url.iloc[:, 0]
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

    print('\nCreate dataframe all words (value.csv):')
    df_words_in_doc = create_df_words(desirialized_articles)

    print('\nView value counts:')
    def view_value_counts(size_of_head):
        for i in range(0, len(df_words_in_doc.columns)):
            print('url №', i, '\n', df_words_in_doc.iloc[:, i].value_counts().head(size_of_head))
    view_value_counts(size_of_head=10)

    print('\nCreate uci from Article (to \'out\'):')
    df_words_in_doc = create_uci(desirialized_articles)

